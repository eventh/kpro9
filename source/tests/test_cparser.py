"""
Module for testing the cparser module.

Tests the C parser, the C preprocessor, and finding structs.
"""
import sys, os
from attest import Tests, assert_hook, reporters
from pycparser import c_ast

# Add the parent folder to path, so we don't need to install our program
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))

import cparser


parse = Tests()

@parse.test
def basic_types():
    """Test that our parser support structs with basic types."""
    ast = cparser.parse('struct simple { int a; float b; char c;};')
    struct = ast.children()[0].children()[0]
    a, b, c = struct.children()

    assert struct.name == 'simple'
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert a.children()[0].children()[0].names[0] == 'int'
    assert b.children()[0].children()[0].names[0] == 'float'
    assert c.children()[0].children()[0].names[0] == 'char'

@parse.test
def array_type():
    """Test arrays as struct members."""
    ast = cparser.parse('struct arr { int a[10]; char b[20]; };')
    struct = ast.children()[0].children()[0]
    a, b = struct.children()

    assert struct.name == 'arr'
    assert isinstance(a.children()[0], c_ast.ArrayDecl)
    assert b.children()[0].children()[0].declname == 'b'
    assert b.children()[0].children()[0].children()[0].names[0] == 'char'


find_structs = Tests()

@find_structs.test
def basic_types():
    """Test that we find structs which has members of basic types."""
    ast = cparser.parse('struct simple { int a; float b; char c;};')
    a, b, c = cparser.find_structs(ast)[0].members
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert a.type == 'int' and b.type == 'float' and c.type == 'char'
    assert a.size == 4 and b.size == 4 and c.size == 1


# Run all tests defined in this module, with PlainReporter
if __name__ == '__main__':
    all_tests = Tests([parse, find_structs])
    all_tests.run(reporters.PlainReporter())

