#! /usr/bin/env python3
"""
A module for creating Wireshark dissectors from C structs.

Usage:
---------
csjark.py [-h] [-verbose] [-debug] [-nocpp]
          [-input [header [header ...]]]
          [-config [config [config ...]]] [-output [output]]
          [header] [config]

positional arguments:
  header                C file to parse
  config                config file to parse

optional arguments:
  -h, --help            show this help message and exit
  -verbose              print detailed information
  -debug                print debugging information
  -nocpp                disable C preprocessor
  -input [header [header ...]]
                        C file(s) to parse
  -config [config [config ...]]
                        configuration file(s) to parse
  -output [output]      write output to file

Example:
"python csjark.py -v -nocpp headerfile.h configfile.yml"
"""
import sys
import os
import argparse

import cparser
import config


class Cli:
    """A class for handling command line interface parsing."""
    verbose = False
    debug = False
    use_cpp = True
    output_dir = None # Store all output in a directory
    output_file = None # Store output in a single file

    @classmethod
    def parse_args(cls, args=None):
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
        parser.add_argument('-verbose', action='store_true',
                default=cls.verbose, help='print detailed information')

        # Debug flag
        parser.add_argument('-debug', action='store_true',
                default=cls.debug, help='print debugging information')

        # No CPP flag
        parser.add_argument('-nocpp', action='store_false', dest='nocpp',
                default=cls.use_cpp, help='disable C preprocessor')

        # A list of C header files
        parser.add_argument('-input', metavar='header',
                default=[], nargs='*', help='C file(s) to parse')

        # Configuration file
        parser.add_argument('-config', metavar='config', dest='configs',
                 default=[], nargs='*', help='configuration file(s) to parse')

        # Write output to destination file
        parser.add_argument('-output', metavar='output',
                nargs='?', help='write output to directory/file')

        # Parse arguments
        if args is None:
            namespace = parser.parse_args()
        else:
            namespace = parser.parse_args(args)

        cls.verbose = namespace.verbose
        cls.debug = namespace.debug
        cls.use_cpp = namespace.nocpp

        # Find out where to store output from the generator
        if namespace.output:
            path = os.path.join(os.path.dirname(sys.argv[0]), namespace.output)
            if os.path.isdir(path):
                cls.output_dir = path
            else:
                cls.output_file = path

        headers = namespace.input
        if namespace.header:
            headers.append(namespace.header)

        configs = namespace.configs
        if namespace.config:
            configs.append(namespace.config)

        # Need to provide either a header file or a config file
        if not headers and not configs:
            parser.print_help()
            sys.exit(2)

        # Make sure the files provided actually exists
        missing = [i for i in headers + configs if
                    os.path.exists(os.path.join(sys.argv[0], i))]
        if missing:
            print('Unknown file(s): %s' % ', '.join(missing))
            sys.exit(2)

        return headers, configs


def create_dissector(filename):
    """Create a Wireshark dissector from 'filename'."""
    ast = cparser.parse_file(filename, use_cpp=Cli.use_cpp)

    if Cli.verbose:
        ast.show()

    protocols = cparser.find_structs(ast)

    # Generate and write lua dissectors
    for proto in protocols:
        code = proto.create()

        if Cli.output_dir:
            path = '%s/%s.lua' % (Cli.output_dir, proto.name)
        elif Cli.output_file:
            path = Cli.output_file
        else:
            path = '%s.lua' % proto.name

        with open(path, 'w') as f:
            f.write(code)

    return len(protocols)


def main():
    """Run the CSjark program."""
    headers, configs = Cli.parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)

        if Cli.verbose:
            print("Parsed config file '%s' successfully." % filename)

    # Create dissectors
    dissectors = 0
    for filename in headers:
        dissectors += create_dissector(filename)

        if Cli.verbose:
            print("Parsed header file '%s' successfully." % filename)

    print("Successfully parsed %i file(s), created %i dissector(s)." % (
            len(headers), dissectors))


if __name__ == "__main__":
    main()

