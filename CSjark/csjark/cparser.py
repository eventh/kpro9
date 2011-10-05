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
from wireshark import create_field, size_of


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
    return visitor.structs


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    def __init__(self):
        self.structs = [] # All structs encountered in this AST

    def visit_Struct(self, node):
        """Visit a Struct node in the AST."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # No support for typedef structs yet!
        if not node.name:
            return

        # Find config rules
        conf = StructConfig.configs.get(node.name, None)

        # Create the protocol for the struct
        if conf:
            proto = Protocol(node.name, conf.id, conf.description)
        else:
            proto = Protocol(node.name)

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
                raise ParseError("Unknown struct member: %s" % repr(child))

        # Don't add protocols with no fields? Sounds reasonably
        if proto.fields:
            self.structs.append(proto)

    def handle_type_decl(self, node, proto, conf):
        """Find member details in a type declaration."""
        child = node.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            ctype = ' '.join(reversed(child.names))
        elif isinstance(child, c_ast.Enum):
            ctype = "enum"
        elif isinstance(child, c_ast.Union):
            ctype = "union"
        elif isinstance(child, c_ast.Struct):
            ctype = "struct"
        else:
            raise ParseError("Unknown type declaration: %s" % repr(child))
        create_field(proto, conf, node.declname, ctype)

    def handle_array_decl(self, node, proto, conf):
        """Find member details in an array declaration."""
        type_decl, constant = node.children()
        child = type_decl.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            if child.names[0] == 'char':
                ctype = 'string'
            else:
                ctype = ' '.join(reversed(child.names))
        else:
            raise ParseError('array of different types not supported yet.')

        if hasattr(constant, 'value'):
            size = int(constant.value) * size_of(ctype)
        else:
            # TODO
            size = 99
            print(constant)
        create_field(proto, conf, type_decl.declname, ctype, size=size)

    def handle_ptr_decl(self, node, proto, conf):
        """Find member details in a pointer declaration."""
        type_decl = node.children()[0]
        ctype = 'pointer' # Shortcut as pointers not a requirement
        create_field(proto, conf, type_decl.declname, ctype)

