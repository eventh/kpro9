#! /usr/bin/env python
"""
A module for creating Wireshark dissectors for C structs.
"""
import sys
import cparser
import dissector
import config


def main():
    if len(sys.argv) < 2:
        print("Please provide a C file to parse")
        sys.exit(2)

    # Parse a config file
    if len(sys.argv) > 2:
        config.parse_file(sys.argv[2])

    # Parse the given C file to create an AST
    filename = sys.argv[1]
    ast = cparser.parse_file(filename)
    ast.show()

    # Recursivly decent AST to find structs
    protocols = cparser.find_structs(ast)

    # Generate and write lua dissectors
    for proto in protocols:
        code = proto.create()
        with open('%s.lua' % proto.name, 'w') as f:
            f.write(code)


if __name__ == "__main__":
    main()

