# -*- coding: utf-8 -*-
# Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
# Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
# Sigurd Wien and Jaroslav Fibichr.
#
# This file is part of CSjark.
#
# CSjark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSjark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSjark.  If not, see <http://www.gnu.org/licenses/>.
"""
Module for testing the cparser module.

Tests the C parser, the C preprocessor, and finding structs.
"""
import sys, os
from attest import Tests, assert_hook, contexts
from pycparser import c_ast

import cpp
import cparser
from platform import Platform


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
def parse_union_type():
    """Test enums as struct members."""
    ast = cparser.parse('''
    union test_union { short a; long long b; float c; };
    struct struct_with_union { union test_union union_member; int d; };
    ''')
    union = ast.children()[0].children()[0]
    a, b, c = union.children()
    assert union.name == 'test_union'
    struct = ast.children()[1].children()[0]
    a, b = struct.children()
    assert struct.name == 'struct_with_union'
    assert isinstance(_child(a, 2), c_ast.Union)
    assert _child(a, 1).declname == 'union_member'
    assert _child(a, 2).name == 'test_union'

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
        long double bytes;
    };
    '''
    ast = cparser.parse(code, 'test')
    structs = {i.name: i for i in cparser.find_structs(ast)}
    yield list(structs['find'].dissectors.values())[0].children
    cparser.StructVisitor.all_protocols = {}

@find_structs.test
def find_basic_types(fields):
    """Test that we find structs which has members of basic types."""
    a, b, c = fields[:3]
    assert a and b and c
    assert a.name == 'a' and b.name == 'b' and c.name == 'c'
    assert a.type == 'int32' and b.type == 'float' and c.type == 'int8'
    assert a.size == 4 and b.size == 4 and c.size == 1

@find_structs.test
def find_enum_types(fields):
    """Test that we find structs which has enums as members."""
    enum = fields[3]
    assert enum.name == 'enumtest'
    assert enum._valuestring_values == '{[0]="RED", [10]="RED", [3]="GREEN", [4]="YELLOW"}'
    assert enum.type == 'uint32' and enum.size == 4

@find_structs.test
def find_array_types(fields):
    """Test that we find structs which has arrays as members."""
    a, b = fields[4:6]
    assert a.name == 'str' and b.name == 'd'
    assert a.type == 'string' and b.type == 'bytes'
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
    assert arr.type == 'bytes'
    assert arr.size == 16

@find_structs.test
def find_struct_typedef_enum(fields):
    """Test that we find typedef enums as array members."""
    enum = fields[8]
    assert enum
    assert enum.name == 'day'
    assert enum.type == 'uint32'
    assert enum.values and enum.list_validation
    assert enum.func_type == 'uint'

@find_structs.test
def find_sturct_wildcard_type(fields):
    """Test that we create field type bytes for unknown types."""
    wildcard = fields[9]
    assert wildcard
    assert wildcard.name == 'bytes'
    assert wildcard.type == 'bytes'
    assert wildcard.size == 8

@find_structs.test
def parse_error():
    """Test that two structs with the same name raises an error."""
    code = 'struct a {int c;}; \nstruct b { int d; \nstruct a {int d;}; };'
    ast = cparser.parse(code, 'test')
    with contexts.raises(cparser.ParseError) as error:
        cparser.find_structs(ast)
    assert str(error).startswith('Two structs with same name a')


# Tests for the C preprocessor
cpps = Tests()

@cpps.context
def create_ast():
    """Parse a C headerfile with C preprocessor, and create an AST."""
    cpp_h = os.path.join(os.path.dirname(__file__), 'cpp.h')
    inc_h = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(cpp_h) and os.path.isfile(inc_h)
    text = cpp.parse_file(cpp_h)
    yield cparser.parse(text)

@cpps.test
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

@cpps.test
def cpp_include(ast):
    """Test that our C preprocessor support #include."""
    a, b, c = ast.children()
    assert _child(c, 5).names[0] == 'bool'
    assert int(_child(c, 3).children()[1].value) == 5

@cpps.test
def cpp_macros(ast):
    """Test that our C preprocessor support _WIN32 and other macros."""
    pass # Meh, how do we solve this?

