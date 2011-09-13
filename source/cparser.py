#! /usr/bin/env python
"""
A module for parsing C files, returns an Abstract Syntax Tree.

Requires PLY and pycparser.
"""
import sys
from pycparser import parse_file


def parse(filename):
    # Portable cpp path for Windows and Linux/Unix
    CPPPATH = './utils/cpp.exe' if sys.platform == 'win32' else 'cpp'

    ast = parse_file(filename, use_cpp=True,
            cpp_path=CPPPATH,
            cpp_args=r'-I/utils/fake_libc_include')

    return ast


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ast = parse(sys.argv[1])
        ast.show()
    else:
        print("Please provide a C file to parse")

