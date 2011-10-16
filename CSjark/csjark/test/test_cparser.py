"""
Module for testing the cparser module.

Tests the C parser, the C preprocessor, and finding structs.
"""
import sys, os
from attest import Tests, assert_hook, contexts
from pycparser import c_ast

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
    struct = _child(ast, 2)
    a, b, c = struct.children()
    assert struct.name == 'simple'
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert _child(a, 2).names[0] == 'int'
    assert _child(b, 2).names[0] == 'float'
    assert _child(c, 2).names[0] == 'char'

@parse.test
def parse_enum_type():
    """Test enums as struct members."""
    ast = cparser.parse('''
    enum color { RED=1, BLUE, GREEN=5 };
    struct arr { enum color which; int tmp; };
    ''')
    struct = ast.children()[1].children()[0]
    a, b = struct.children()
    assert struct.name == 'arr'
    assert isinstance(_child(a, 2), c_ast.Enum)
    assert _child(a, 1).declname == 'which'
    assert _child(a, 2).name == 'color'

@parse.test
def parse_array_type():
    """Test arrays as struct members."""
    ast = cparser.parse('struct arr { int a[10]; char b[20]; };')
    struct = _child(ast, 2)
    a, b = struct.children()
    assert struct.name == 'arr'
    assert isinstance(_child(a, 1), c_ast.ArrayDecl)
    assert _child(b, 2).declname == 'b'
    assert _child(b, 3).names[0] == 'char'


# Tests for cparser.find_structs()
find_structs = Tests()

@find_structs.context
def create_structs():
    """Creates an AST and finds all structs within it."""
    code = '''
    struct inner {
        int a1;
        int a2;
        int a3;
    };
    enum color { RED, GREEN=3, YELLOW, RED=10 };
    typedef enum weekday { MON, TUE, WED, FRI=5 } weekday_t;
    struct find {
        int a; float b; char c;
        enum color enumtest;
        char str[30]; float d[3];
        struct inner inner_struct;
        unsigned short oprs[+2][9-7][((5 * 3) + (-5)) / 5];
        weekday_t day;
    };
    '''
    ast = cparser.parse(code, 'test')
    yield cparser.find_structs(ast)[1].fields
    del cparser.StructVisitor.all_structs['find']

@find_structs.test
def find_basic_types(fields):
    """Test that we find structs which has members of basic types."""
    a, b, c = fields[:3]
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert a.type == 'int32' and b.type == 'float' and c.type == 'string'
    assert a.size == 4 and b.size == 4 and c.size == 1

@find_structs.test
def find_enum_types(fields):
    """Test that we find structs which has enums as members."""
    enum = fields[3]
    assert enum.name == 'enumtest'
    assert enum.values == '{[0]="RED", [10]="RED", [3]="GREEN", [4]="YELLOW"}'
    assert enum.type == 'uint32' and enum.size == 4

@find_structs.test
def find_array_types(fields):
    """Test that we find structs which has arrays as members."""
    a, b = fields[4:6]
    assert a.name == 'str' and b.name == 'd'
    assert a.type == 'string' and b.type == 'float'
    assert a.size == 30 and b.size == 12

@find_structs.test
def find_struct_types(fields):
    """Test that we find structs which has arrays as members."""
    a = fields[6]
    assert a.name == 'inner_struct'
    assert a.type == 'inner'
    assert a.size == 12

@find_structs.test
def find_struct_array_math(fields):
    """Test that expressions in array declarations are evaluated."""
    arr = fields[7]
    assert arr.name == 'oprs'
    assert arr.type == 'uint16'
    assert arr.size == 16

@find_structs.test
def find_struct_typedef_enum(fields):
    """Test that we find typedef enums as array members."""
    enum = fields[8]
    assert enum
    assert enum.name == 'day'
    assert enum.type == 'uint32'
    assert enum.values and enum.keys
    assert enum.func_type == 'uint'

@find_structs.test
def parse_error():
    """Test that two structs with the same name raises an error."""
    code = 'struct a {int c;}; \nstruct b { int d; \nstruct a {int d;}; };'
    ast = cparser.parse(code, 'test')
    with contexts.raises(cparser.ParseError) as error:
        cparser.find_structs(ast)
    assert str(error).startswith('Two structs with same name a')


# Tests for the C preprocessor
cpp = Tests()

@cpp.context
def create_ast():
    """Parse a C headerfile with C preprocessor, and create an AST."""
    cpp_h = os.path.join(os.path.dirname(__file__), 'cpp.h')
    inc_h = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(cpp_h) and os.path.isfile(inc_h)
    yield cparser.parse_file(cpp_h)

@cpp.test
def cpp_define(ast):
    """Test that our C preprocessor support #define."""
    assert ast
    a, b, c = ast.children()
    assert _child(b, 1).name == 'simple'
    assert _child(b, 2).name == 'arr'
    assert isinstance(_child(b, 3), c_ast.ArrayDecl)
    type_decl, constant = _child(b, 3).children()
    assert constant.type == 'int'
    assert int(constant.value) == 10

@cpp.test
def cpp_include(ast):
    """Test that our C preprocessor support #include."""
    a, b, c = ast.children()
    assert _child(c, 5).names[0] == 'bool'
    assert int(_child(c, 3).children()[1].value) == 5

