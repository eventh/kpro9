#! /usr/bin/env python3
"""
A module for creating Wireshark dissectors from C structs.

Usage:
csjark.py [-h] [-v] [-d] [-s] [-f [header [header ...]]]
          [-c [config [config ...]]] [-o [output]] [-p] [-n] [-C [cpp]]
          [-i [header [header ...]]] [-I [directory [directory ...]]]
          [-D [name=definition [name=definition ...]]]
          [-U [name [name ...]]] [-A [argument [argument ...]]]
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
  -s, --strict          Only generate dissectors for known structs
  -p, --placeholders    Generate placeholder config file for unknown structs

Example:
"python csjark.py -v -nocpp headerfile.h configfile.yml"
"""
import sys
import os
import argparse

import cpp
import cparser
import config
from config import Options, FileConfig


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

    # Strict flag, not in use yet
    parser.add_argument('-s', '--strict', action='store_true',
            default=Options.strict,
            help='Only generate dissectors for known structs')

    # A list of C header files
    parser.add_argument('-f', '--file', metavar='header',
            default=[], nargs='*', help='C header or code file(s) to parse')

    # Configuration file
    parser.add_argument('-c', '--config', metavar='config', dest='configs',
            default=[], nargs='*', help='configuration file(s) to parse')

    # Write output to destination file
    parser.add_argument('-o', '--output', metavar='output',
            nargs='?', help='write output to directory/file')

    # Generate placeholder config files
    parser.add_argument('-p', '--placeholders', action='store_true',
            default=Options.generate_placeholders,
            help='Generate placeholder config file for unknown structs')

    # No CPP flag
    parser.add_argument('-n', '--nocpp', action='store_false', dest='nocpp',
            default=Options.use_cpp, help='disable C preprocessor')

    # Argument for specifying which CPP to use
    parser.add_argument('-C', '--CPP', metavar='cpp',
            nargs='?', help='Which C preprocessor to use')

    # CPP include arguments
    parser.add_argument('-i', '--include', metavar='header', default=[],
            nargs='*', help='Process file as Cpp #include "file" directive')

    # CPP Includes directories arguments
    parser.add_argument('-I', '--Includes', metavar='directory', default=[],
            nargs='*', help='Directories to be searched for Cpp includes')

    # CPP Define macro arguments
    parser.add_argument('-D', '--Define', metavar='name=definition',
            default=[], nargs='*', help='Predefine name as a Cpp macro')

    # CPP Undefine macro arguments
    parser.add_argument('-U', '--Undefine', metavar='name', default=[],
            nargs='*', help='Cancel any previous Cpp definition of name')

    # Additional CPP arguments
    parser.add_argument('-A', '--Additional', metavar='argument', default=[],
            nargs='*', help='Any additional C preprocessor arguments')

    # Parse arguments
    if args is None:
        namespace = parser.parse_args()
    else:
        namespace = parser.parse_args(args)

    # Store options
    Options.verbose = namespace.verbose
    Options.debug = namespace.debug
    Options.strict = namespace.strict
    Options.generate_placeholders = namespace.placeholders
    Options.use_cpp = namespace.nocpp
    Options.cpp_path = namespace.CPP
    Options.default.includes = namespace.include
    Options.default.include_dirs = namespace.Includes
    Options.default.defines = namespace.Define
    Options.default.undefines = namespace.Undefine
    Options.default.args = namespace.Additional

    headers = namespace.file
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
                folder = var.pop(i)
                var.extend(os.path.join(folder, path) for path in
                        os.listdir(folder) if os.path.isdir(path)
                        or os.path.splitext(path)[1] in file_extensions)
            else:
                i += 1

    files_in_folder(headers, ('.h', '.hpp', '.c'))
    files_in_folder(configs, ('.yml', ))

    return headers, configs


def parse_headers(headers):
    """Parse 'headers' to create a Wireshark protocol dissector."""
    def decode_error(error, platform):
        msg = str(error)
        if 'before: ' in msg:
            key = msg.rsplit('before: ', 1)[1].strip(), platform
            return cparser.StructVisitor.all_known_types.get(key, None)

    # First try, in the order given through the CLI
    failed = [] # Protocols we have failed to generate
    for filename in headers:
        for platform in Options.platforms:
            error = create_dissector(filename, platform)
            if error is not None:
                failed.append([filename, platform, error])

    # Second try, include the missing file
    for i in reversed(range(len(failed))):
        filename, platform, error = failed[i]
        include = decode_error(error, platform)
        if include is not None:
            if os.path.normpath(filename) == os.path.normpath(include):
                continue # Problem with typedef, impossibru!
            new_error = create_dissector(filename, platform, [include])
            if new_error != error:
                FileConfig.add_include(filename, include)
                failed[i][2] = new_error
            if new_error is None:
                failed.pop(i)

    # Third try, include all who worked as it might help
    failed_names = [filename for filename, platform, error in failed]
    includes = [file for file in headers if file not in failed_names]
    for i in reversed(range(len(failed))):
        filename, platform, tmp = failed.pop(i)
        error = create_dissector(filename, platform, includes)
        if error is None:
            # Worked, record it in case anyone else needs this file
            for inc in includes:
                FileConfig.add_include(filename, inc)
            includes.append(filename)
        else:
            failed.append([filename, platform, error])

    # Potential for a fourth and fifth try

    # Give up!
    for filename, platform, error in failed:
        print('Skipped "%s":%s as it raised %s' % (
                filename, platform.name, repr(error)))


def create_dissector(filename, platform, includes=None):
    """Parse 'filename' to create a Wireshark protocol dissector.

    'filename' is the C header/code file to parse.
    'platform' is the platform we should simulate.
    'includes' is a set of filenames to #include.
    Returns the error if parsing failed, None if succeeded.
    """
    try:
        text = cpp.parse_file(filename, platform, includes)
        ast = cparser.parse(text, filename)
        cparser.find_structs(ast, platform)
    except Exception as err:
        if Options.verbose:
            print('Failed "%s":%s which raised %s' % (
                    filename, platform.name, repr(err)))
        if Options.debug:
            sys.excepthook(*sys.exc_info())
        return err

    if Options.verbose:
        print("Parsed header file '%s':%s successfully." % (
                filename, platform.name))

    if Options.debug:
        ast.show()


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
            print("Wrote %s to '%s' (%i platform(s))" %
                    (name, path, len(protos)))


def write_delegator_to_file():
    """Write the lua file which delegates dissecting to dissectors."""
    filename = 'luastructs.lua'
    if Options.output_dir:
        filename = '%s/%s' % (Options.output_dir, filename)

    with open(filename, 'w') as f:
        f.write(Options.delegator.create())

    if Options.verbose:
        print("Wrote delegator file to '%s'" % filename)


def write_placeholders_to_file(protocols):
    """Write a placeholder file for 'protocols' with no configuration."""
    if not protocols or not Options.generate_placeholders:
        return

    text, count = config.generate_placeholders(protocols)
    filename = 'placeholders.yml'
    with open(filename, 'w') as f:
        f.write(text)

    if Options.verbose:
        print("Wrote %i config placeholders to '%s'" % (count, filename))


def main():
    """Run the CSjark program."""
    headers, configs = parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)
    Options.prepare_for_parsing()

    # Parse all headers to create protocols
    parse_headers(headers)

    # Write dissectors to disk
    protocols = cparser.StructVisitor.all_protocols
    write_dissectors_to_file(protocols)
    write_delegator_to_file()
    write_placeholders_to_file(protocols)

    print("Successfully parsed %i file(s), created %i dissector(s)." % (
            len(headers), len(protocols)))


if __name__ == "__main__":
    main()

