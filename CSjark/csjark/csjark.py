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
import dissector


class Cli:
    """A class for handling command line interface parsing."""
    verbose = False
    debug = False
    use_cpp = True

    @classmethod
    def parse_args(cls):
        """Parse arguments given in sys.argv."""
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
        parser.add_argument('-nocpp', action='store_false', dest='cpp',
                default=cls.use_cpp, help='disable C preprocessor')

        # A list of C header files
        parser.add_argument('-input', metavar='header',
                default=[], nargs='*', help='C file(s) to parse')

        # Configuration file
        parser.add_argument('-config', metavar='config', dest='configs',
                 default=[], nargs='*', help='configuration file(s) to parse')

        # Write output to destination file
        parser.add_argument('-output', metavar='output',
                nargs='?', help='write output to file')

        # Parse arguments
        args = parser.parse_args()

        cls.verbose = args.verbose
        cls.debug = args.debug
        cls.use_cpp = args.cpp

        headers = args.input
        if args.header:
            headers.append(args.header)

        configs = args.configs
        if args.config:
            configs.append(args.config)

        # Need to provide either a header file or a config file
        if len(sys.argv) < 2 or (not headers and not configs):
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
        with open('%s.lua' % proto.name, 'w') as f:
            f.write(code)


def main():
    """Run the CSjark program."""
    headers, configs = Cli.parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)

        if Cli.verbose:
            print("Parsed config file '%s' successfully." % filename)

    # Create dissectors
    for filename in headers:
        create_dissector(filename)

        if Cli.verbose:
            print("Parsed header file '%s' successfully." % filename)


if __name__ == "__main__":
    main()

