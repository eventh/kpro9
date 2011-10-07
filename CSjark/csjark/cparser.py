#! /usr/bin/env python
"""
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import sys
import os

import pycparser
from pycparser import c_ast, c_parser, plyparser

from config import StructConfig
from dissector import Protocol
from wireshark import size_of, create_field, create_enum


class ParseError(plyparser.ParseError):
    """Exception raised by invalid input to the parser."""
    pass


def parse_file(filename, use_cpp=True, fake_includes=True, cpp_path=None):
    """Parse a C file, returns abstract syntax tree.

    use_cpp: Enable or disable the C preprocessor
    fake_includes: Add fake includes for libc header files
    cpp_path: The path to cpp.exe on windows
    """
    cpp_args = None
    if cpp_path is None:
        cpp_path = 'cpp'

    if use_cpp:
        cpp_args = []

        if fake_includes:
            cpp_args.append(r'-I../utils/fake_libc_include')

        if os.path.dirname(filename):
            cpp_args.append(r'-I%s' % os.path.dirname(filename))

        # TODO: find a cleaner way to look for cpp on windows!
        if sys.platform == 'win32' and cpp_path == 'cpp':
            cpp_path = '../utils/cpp.exe' # Windows don't come with a CPP
        elif sys.platform == 'darwin':
            cpp_path = 'gcc' # Fix for a bug in Mac GCC 4.2.1
            cpp_args.append('-E')

    # Generate an abstract syntax tree
    ast = pycparser.parse_file(filename, use_cpp=use_cpp,
            cpp_path=cpp_path, cpp_args=cpp_args)

    return ast


def parse(text, filename=''):
    """Parse C code and return an AST."""
    parser = c_parser.CParser()
    return parser.parse(text, filename)


def find_structs(ast):
    """Walks the AST nodes to find structs."""
    visitor = StructVisitor()
    visitor.visit(ast)
    return list(visitor.structs.values())


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    def __init__(self):
        self.structs = {} # All structs encountered in this AST
        self.enums = {} # All enums encountered in this AST
        self.aliases = {} # Typedefs and their base type
        self.type_decl = [] # Queue of current type declaration

    def _get_type(self, node):
        """Get the C type from a node."""
        return ' '.join(reversed(node.names))

    def visit_Struct(self, node):
        """Visit a Struct node in the AST."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # No children, its a member and not a declaration
        if not node.children():
            return

        # Typedef structs
        if not node.name:
            node.name = self.type_decl[-1]
        print(node.name)

        # Find config rules
        conf = StructConfig.configs.get(node.name, None)

        # Create the protocol for the struct
        if conf:
            proto = Protocol(node.name, conf.id, conf.description)
        else:
            proto = Protocol(node.name)
        proto._coord = node.coord

        # Find the member definitions
        for decl in node.children():
            child = decl.children()[0]

            if isinstance(child, c_ast.TypeDecl):
                self.handle_type_decl(child, proto, conf)
            elif isinstance(child, c_ast.ArrayDecl):
                self.handle_array_decl(child, proto, conf)
            elif isinstance(child, c_ast.PtrDecl):
                self.handle_ptr_decl(child, proto, conf)
            else:
                raise ParseError('Unknown struct member: %s' % repr(child))

        # Disallow structs with same name
        if node.name in self.structs:
            other = self.structs[node.name]
            raise ParseError('Two structs with same name: %s in %s:%i & %s:%i'
                    % (node.name, other._coord.file,
                        other._coord.line, node.coord.file, node.coord.line))

        # Don't add protocols with no fields? Sounds reasonably
        if proto.fields:
            self.structs[node.name] = proto

    def visit_Enum(self, node):
        """Visit a Enum node in the AST."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # Empty Enum definition or using Enum
        if not node.children():
            return

        # Find id:name of members
        members = {}
        i = -1
        for child in node.children()[0].children():
            if child.children():
                i = int(child.children()[0].value)
            else:
                i += 1
            members[i] = child.name

        self.enums[node.name] = members

    def visit_Typedef(self, node):
        """Visit Typedef declarations nodes in the AST."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # Find the type
        child = node.children()[0].children()[0]
        if isinstance(child, c_ast.IdentifierType):
            type = self._get_type(child)
            type = self.aliases.get(type, type)
            self.aliases[node.name] = type

    def visit_TypeDecl(self, node):
        """Keep track of Type Declaration nodes."""
        self.type_decl.append(node.declname)
        c_ast.NodeVisitor.generic_visit(self, node)
        self.type_decl.pop()

    def handle_type_decl(self, node, proto, conf):
        """Find member details in a type declaration."""
        child = node.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            ctype = self._get_type(child)
            create_field(proto, conf, node.declname, ctype)
        elif isinstance(child, c_ast.Enum):
            if child.name not in self.enums.keys():
                raise ParseError('Unknown enum: %s' % child.name)
            create_enum(proto, conf, node.declname, self.enums[child.name])
        elif isinstance(child, c_ast.Union):
            create_field(proto, conf, node.declname, 'union')
        elif isinstance(child, c_ast.Struct):
            create_field(proto, conf, node.declname, 'struct')
        else:
            raise ParseError('Unknown type declaration: %s' % repr(child))

    def handle_array_decl(self, node, proto, conf):
        """Find member details in an array declaration."""
        type_decl, constant = node.children()
        child = type_decl.children()[0]

        # TODO: support multidimentional arrays.
        if isinstance(type_decl, c_ast.ArrayDecl):
            return

        # Calculate size of the array
        if isinstance(constant, c_ast.Constant):
            arr_size = int(constant.value)
        elif isinstance(constant, c_ast.BinaryOp):
            arr_size = 0 # TODO: evaluate BinaryOp expression
        elif isinstance(constant, c_ast.ID):
            arr_size = 0 # TODO? PATH_MAX WTF?
        else:
            print(constant)
            raise ParseError('array of different types not supported yet.')

        # Create suiteable field for the array
        if child.names[0] == 'char':
            size = arr_size * size_of('char')
            create_field(proto, conf, type_decl.declname, 'string', size)
        else:
            type = self._get_type(child)
            size = arr_size * size_of(type)
            create_field(proto, conf, type_decl.declname, 'todo', size)

    def handle_ptr_decl(self, node, proto, conf):
        """Find member details in a pointer declaration."""
        type_decl = node.children()[0]
        ctype = 'pointer' # Shortcut as pointers not a requirement
        create_field(proto, conf, type_decl.declname, ctype)

