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


def _child(node, depth=1):
    """Find a child in the AST, by depth first."""
    child = node
    while depth > 0:
        child = child.children()[0]
        depth -= 1
    return child

# Tests for cparser.parse()
parse = Tests()

@parse.test
def parse_basic_types():
    """Test that our parser support structs with basic types."""
    ast = cparser.parse('struct simple { int a; float b; char c;};')
    struct = ast.children()[0].children()[0]
    a, b, c = struct.children()

    assert struct.name == 'simple'
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert _child(a, 2).names[0] == 'int'
    assert _child(b, 2).names[0] == 'float'
    assert _child(c, 2).names[0] == 'char'

@parse.test
def parse_array_type():
    """Test arrays as struct members."""
    ast = cparser.parse('struct arr { int a[10]; char b[20]; };')
    struct = ast.children()[0].children()[0]
    a, b = struct.children()

    assert struct.name == 'arr'
    assert isinstance(a.children()[0], c_ast.ArrayDecl)
    assert _child(b, 2).declname == 'b'
    assert _child(b, 3).names[0] == 'char'


# Tests for cparser.find_structs()
find_structs = Tests()

@find_structs.context
def create_structs():
    """Creates an AST and finds all structs within it."""
    code = '''
    struct find {
        int a; float b; char c;
        char str[30]; float d[3];
    };
    '''
    ast = cparser.parse(code, 'test')
    yield cparser.find_structs(ast)[0].members

@find_structs.test
def find_basic_types(structs):
    """Test that we find structs which has members of basic types."""
    a, b, c = structs[:3]
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert a.type == 'int' and b.type == 'float' and c.type == 'char'
    assert a.size == 4 and b.size == 4 and c.size == 1

@find_structs.test
def find_array_types(structs):
    a, b = structs[3:5]
    assert a.name == 'str' and b.name == 'd'
    assert a.type == 'char' and b.type == 'float'


# Run all tests defined in this module, with PlainReporter
if __name__ == '__main__':
    all_tests = Tests([parse, find_structs])
    all_tests.run(reporters.PlainReporter())

