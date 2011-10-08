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
from wireshark import size_of, create_field, create_enum, create_array


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

        # Create the protocol for the struct
        conf = StructConfig.configs.get(node.name, None)
        proto = Protocol(node.name, node.coord, conf)

        # Find the member definitions
        for decl in node.children():
            child = decl.children()[0]

            if isinstance(child, c_ast.TypeDecl):
                self.handle_type_decl(child, proto)
            elif isinstance(child, c_ast.ArrayDecl):
                self.handle_array_decl(child, proto)
            elif isinstance(child, c_ast.PtrDecl):
                self.handle_ptr_decl(child, proto)
            else:
                raise ParseError('Unknown struct member: %s' % repr(child))

        # Disallow structs with same name
        if node.name in self.structs:
            other = self.structs[node.name]
            raise ParseError('Two structs with same name: %s in %s:%i & %s:%i'
                    % (node.name, other.coord.file,
                        other.coord.line, node.coord.file, node.coord.line))

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

    def handle_type_decl(self, node, proto):
        """Find member details in a type declaration."""
        child = node.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            ctype = self._get_type(child)
            create_field(proto, node.declname, ctype)
        elif isinstance(child, c_ast.Enum):
            if child.name not in self.enums.keys():
                raise ParseError('Unknown enum: %s' % child.name)
            create_enum(proto, node.declname, self.enums[child.name])
        elif isinstance(child, c_ast.Union):
            create_field(proto, node.declname, 'union')
        elif isinstance(child, c_ast.Struct):
            create_field(proto, node.declname, 'struct')
        else:
            raise ParseError('Unknown type declaration: %s' % repr(child))

    def _get_array_size(self, node):
        """Calculate the size of the array."""
        child = node.children()[1]

        if isinstance(child, c_ast.Constant):
            size = int(child.value)
        elif isinstance(child, c_ast.BinaryOp):
            size = 0 # TODO: evaluate BinaryOp expression
        elif isinstance(child, c_ast.ID):
            size = 0 # TODO: PATH_MAX WTF?
        else:
            raise ParseError('This type of array not supported: %s' % node)

        return size

    def handle_array_decl(self, node, proto, depth=None):
        """Find member details in an array declaration."""
        if depth is None:
            depth = []
        child = node.children()[0]

        # Multidimensional array or string array
        if isinstance(child, c_ast.ArrayDecl):
            # String array
            if (isinstance(child.children()[0], c_ast.TypeDecl) and
                    child.children()[0].children()[0].names[0] == 'char'):
                size = self._get_array_size(child) * size_of('char')
                if depth:
                    create_array(proto, child.declname, 'string', size, depth)
                else:
                    create_field(proto, child.declname, 'string', size)

            # Multidimensional, handle recursively
            else:
                depth.append(self._get_array_size(node))
                self.handle_array_decl(child, proto, depth)

        # Single dimensional normal array
        else:
            type = self._get_type(child.children()[0])
            size = self._get_array_size(node) * size_of(type)
            create_array(proto, child.declname, type, size, depth)

    def handle_ptr_decl(self, node, proto):
        """Find member details in a pointer declaration."""
        create_field(proto, node.children()[0].declname, 'pointer')

