#! /usr/bin/env python
"""
TODO
"""
import sys
from pycparser import parse_file
import lua


def main():
    if len(sys.argv) < 2:
        print("Please provide a file to parse")
        exit()

    filename = sys.argv[1]

    # Portable cpp path for Windows and Linux/Unix
    CPPPATH = './utils/cpp.exe' if sys.platform == 'win32' else 'cpp'

    ast = parse_file(filename, use_cpp=True,
            cpp_path=CPPPATH,
            cpp_args=r'-I/utils/fake_libc_include')

    ast.show()

    members = {"type": "int", "name": "char", "time": "int"}
    lua.create("test.lua", "internal_snd", members)

if __name__ == "__main__":
    main()

