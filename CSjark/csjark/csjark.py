#! /usr/bin/env python3
"""
A module for creating Wireshark dissectors from C structs.
"""
import sys
import os
import argparse

import cparser
import config
import dissector


class Cli:
    verbose = False
    debug = False


def parse_args():
    parser = argparse.ArgumentParser(
            description='Generate Wireshark dissectors from C structs.')

    parser.add_argument('header', nargs='?')

    # Verbose flag
    parser.add_argument('-verbose', action='store_true',
            help='Print information about AST tree, ect.')

    # Debug flag
    parser.add_argument('-debug', action='store_true', help='Enable debugger')

    # No CPP flag
    parser.add_argument('-nocpp', action='store_false',
            dest='cpp', help='Disable C preprocessor')

    # C-header file
    parser.add_argument('-ch', '--cheader',
            nargs='*', help='C-header file to parse')

    # Configuration file
    parser.add_argument('-c', '--config',
            nargs='*', help='Configuration file to parse')

    # Write output to destination file
    parser.add_argument('-output', nargs='?', help='Write output to file')

    # Parse arguments
    args = parser.parse_args()

    Cli.verbose = args.verbose
    Cli.debug = args.debug

    headers = []
    if args.header:
        headers.append(args.header)
    if args.cheader:
        headers.extend(args.cheader)

    if args.config:
        configs = args.config
    else:
        configs = []

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

    return headers, configs, args.cpp


def create_dissector(filename, use_cpp):
    ast = cparser.parse_file(filename, use_cpp=use_cpp)

    if Cli.verbose:
        ast.show()

    protocols = cparser.find_structs(ast)

    # Generate and write lua dissectors
    for proto in protocols:
        code = proto.create()
        with open('%s.lua' % proto.name, 'w') as f:
            f.write(code)


def main():
    headers, configs, cpp = parse_args()

    # Parse config files
    for filename in configs:
        config.parse_file(filename)

        if Cli.verbose:
            print("Parsed config file '%s' successfully." % filename)

    # Create dissectors
    for filename in headers:
        create_dissector(filename, cpp)

        if Cli.verbose:
            print("Parsed header file '%s' successfully." % filename)


if __name__ == "__main__":
    main()

