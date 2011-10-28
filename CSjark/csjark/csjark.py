#! /usr/bin/env python3
"""
A module for creating Wireshark dissectors from C structs.

Usage:
---------
csjark.py [-h] [-v] [-d] [-n] [-I [include [include ...]]]
          [-i [header [header ...]]] [-c [config [config ...]]]
          [-o [output]]
          [header] [config]

Generate Wireshark dissectors from C structs.

positional arguments:
  header                C file to parse
  config                config file to parse

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print detailed information
  -d, --debug           print debugging information
  -n, --nocpp           disable C preprocessor
  -I [include [include ...]], --Include [include [include ...]]
                        C preprocessor includes
  -i [header [header ...]], --input [header [header ...]]
                        C file(s) to parse
  -c [config [config ...]], --config [config [config ...]]
                        configuration file(s) to parse
  -o [output], --output [output]
                        write output to directory/file

Example:
"python csjark.py -v -nocpp headerfile.h configfile.yml"
"""
import sys
import os
import argparse

import cparser
import config
from config import Options


def parse_args(args=None):
    """Parse arguments given in sys.argv.

    'args' is a list of strings to parse instead of sys.argv.
    """
    parser = argparse.ArgumentParser(
            description='Generate Wireshark dissectors from C structs.')

    # A single C header file
    parser.add_argument('header', nargs='?', help='C file to parse')

    # A single config file
    parser.add_argument('config', nargs='?', help='config file to parse')

    # Verbose flag
    parser.add_argument('-v', '--verbose', action='store_true',
            default=Options.verbose, help='print detailed information')

    # Debug flag
    parser.add_argument('-d', '--debug', action='store_true',
            default=Options.debug, help='print debugging information')

    # No CPP flag
    parser.add_argument('-n', '--nocpp', action='store_false', dest='nocpp',
            default=Options.use_cpp, help='disable C preprocessor')

    # CPP include arguments
    parser.add_argument('-I', '--Include', metavar='include',
            default=[], nargs='*', help='C preprocessor includes')

    # A list of C header files
    parser.add_argument('-i', '--input', metavar='header',
            default=[], nargs='*', help='C file(s) to parse')

    # Configuration file
    parser.add_argument('-c', '--config', metavar='config', dest='configs',
            default=[], nargs='*', help='configuration file(s) to parse')

    # Write output to destination file
    parser.add_argument('-o', '--output', metavar='output',
            nargs='?', help='write output to directory/file')

    # Parse arguments
    if args is None:
        namespace = parser.parse_args()
    else:
        namespace = parser.parse_args(args)

    # Store options
    Options.verbose = namespace.verbose
    Options.debug = namespace.debug
    Options.use_cpp = namespace.nocpp
    Options.cpp_includes = namespace.Include

    headers = namespace.input
    if namespace.header:
        headers.append(namespace.header)

    configs = namespace.configs
    if namespace.config:
        configs.append(namespace.config)

    # If only a .yml file is given, move it to configs
    if len(headers) == 1 and not configs and headers[0][-4:] == '.yml':
        configs.append(headers.pop())

    # Find out where to store output from the generator
    if namespace.output:
        path = os.path.join(os.path.dirname(sys.argv[0]), namespace.output)
        if os.path.isdir(path):
            Options.output_dir = path
        else:
            Options.output_file = path

    # Need to provide either a header file or a config file
    if not headers and not configs:
        parser.print_help()
        sys.exit(2)

    # Make sure the files provided actually exists
    missing = [i for i in headers + configs if not os.path.exists(i)]
    if missing:
        print('Unknown file(s): %s' % ', '.join(missing))
        sys.exit(2)

    # Add files if headers or configs contain folders
    def files_in_folder(var, file_extensions):
        i = 0
        while i < len(var):
            if os.path.isdir(var[i]):
                Options.strict = False # Batch processing
                folder = var.pop(i)
                var.extend(os.path.join(folder, path) for path in
                        os.listdir(folder) if os.path.isdir(path)
                        or os.path.splitext(path)[1] in file_extensions)
            else:
                i += 1

    files_in_folder(headers, ('.h', '.c'))
    files_in_folder(configs, ('.yml', ))

    return headers, configs


def create_dissectors(filename):
    """Parse 'filename' to create a Wireshark protocol dissector."""
    # Handle different platforms
    for platform in Options.platforms:

        # Parse the filename and find all struct definitions
        try:
            ast = cparser.parse_file(filename, platform)
            cparser.find_structs(ast, platform)

        # Silence errors if not in strict mode
        except Exception as err:
            if Options.strict:
                raise
            else:
                print('Skipped "%s":%s as it raised %s' % (
                        filename, platform.name, repr(err)))
                if Options.debug:
                    sys.excepthook(*sys.exc_info())
                    print()
                continue

    if Options.debug:
        ast.show()

    if Options.verbose:
        print("Parsed header file '%s' successfully." % filename)


def write_dissectors_to_file(all_protocols):
    """Write lua dissectors to file(s)."""
    # Delete output_file if it already exists
    if Options.output_file and os.path.isfile(Options.output_file):
        os.remove(Options.output_file)

    # Sort the protocols on name
    sorted_protos = {}
    for key, proto in all_protocols.items():
        if proto.name not in sorted_protos:
            sorted_protos[proto.name] = []
        sorted_protos[proto.name].append(proto)

    # Generate and write lua dissectors
    for name, protos in sorted_protos.items():
        dissectors = [p.create() for p in protos]

        path = '%s.lua' % name
        flag = 'w'
        if Options.output_dir:
            path = '%s/%s' % (Options.output_dir, path)
        elif Options.output_file:
            path = Options.output_file
            flag = 'a'

        with open(path, flag) as f:
            f.write('\n\n'.join(dissectors))

        if Options.verbose:
            print('Wrote %s to %s (%i platforms)' % (name, path, len(protos)))


def write_delegator_to_file():
    """Write the lua file which delegates dissecting to dissectors."""
    filename = 'luastructs.lua'
    if Options.output_dir:
        filename = '%s/%s' % (Options.output_dir, filename)

    with open(filename, 'w') as f:
        f.write(Options.delegator.create())


def main():
    """Run the CSjark program."""
    headers, configs = parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)
    Options.prepare_for_parsing()

    # Create protocols
    for filename in headers:
        create_dissectors(filename)

    # Write dissectors to disk
    protocols = cparser.StructVisitor.all_protocols
    write_dissectors_to_file(protocols)
    write_delegator_to_file()

    print("Successfully parsed %i file(s), created %i dissector(s)." % (
            len(headers), len(protocols)))


if __name__ == "__main__":
    main()

