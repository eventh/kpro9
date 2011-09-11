#! /usr/bin/env python
"""
A module for creating Wireshark dissectors for C structs.
"""
import sys
import cparser
import cstruct
import lua


def main():
    if len(sys.argv) < 2:
        print("Please provide a C file to parse")
        exit()

    # Parse the given C file to create an AST
    filename = sys.argv[1]
    ast = cparser.parse(filename)
    ast.show()

    # Recursivly decent AST to find structs
    structs = cstruct.find_structs(ast)

    # Generate lua dissectors
    lua.write(structs)

if __name__ == "__main__":
    main()

