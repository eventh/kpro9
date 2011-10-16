"""
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import sys
import os
import operator

import pycparser
from pycparser import c_ast, c_parser, plyparser

from config import size_of, map_type, StructConfig
from dissector import Protocol


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

    all_structs = {} # Map struct names and their protocol

    def __init__(self):
        self.structs = [] # All structs encountered in this AST
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
        if node.name in StructVisitor.all_structs:
            o = StructVisitor.all_structs[node.name].coord
            if (os.path.normpath(o.file) != os.path.normpath(node.coord.file)
                    or o.line != node.coord.line):
                raise ParseError('Two structs with same name %s: %s:%i & %s:%i' % (
                       node.name, o.file, o.line, node.coord.file, node.coord.line))

        # Don't add protocols with no fields? Sounds reasonably
        if proto.fields:
            self.structs.append(proto)
            self.all_structs[node.name] = proto

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
            ctype = self._get_type(child)
            self.aliases[node.name] = self.aliases.get(ctype, (ctype, None))
        elif isinstance(child, c_ast.Enum):
            self.aliases[node.name] = (child.name, 'enum')
        elif isinstance(child, c_ast.Struct):
            self.aliases[node.name] = (child.name, 'struct')
        elif isinstance(child, c_ast.Union):
            self.aliases[node.name] = (child.name, 'union')
        #elif isinstance(node.children()[0], c_ast.ArrayDecl):
        #    pass # TODO
        else:
            print(node, node.name, child) # For testing purposes
            raise ParseError('Unknown typedef type: %s' % child)

    def visit_TypeDecl(self, node):
        """Keep track of Type Declaration nodes."""
        self.type_decl.append(node.declname)
        c_ast.NodeVisitor.generic_visit(self, node)
        self.type_decl.pop()

    def handle_type_decl(self, node, proto):
        """Find member details in a type declaration."""
        child = node.children()[0]

        # Identifier member, simple type or typedef type
        if isinstance(child, c_ast.IdentifierType):
            ctype = self._get_type(child)

            # Typedef type, which is an alias for another type
            if ctype in self.aliases:
                base, token = self.aliases[ctype]
                if token == 'enum':
                    self.handle_enum(proto, node.declname, base)
                elif token == 'struct':
                    self.handle_struct(proto, node.declname, base)
                else:
                    # If any rules exists, use new type and not base
                    if proto.conf and proto.conf.get_rules(None, ctype):
                        base = ctype # Is this wise?
                    self.add_field(proto, node.declname, base)
            else:
                self.add_field(proto, node.declname, ctype)

        # Enum member
        elif isinstance(child, c_ast.Enum):
            self.handle_enum(proto, node.declname, child.name)
        # Union member
        elif isinstance(child, c_ast.Union):
            self.add_field(proto, node.declname, 'union')
        # Struct member
        elif isinstance(child, c_ast.Struct):
            self.handle_struct(proto, node.declname, child.name)
        # Error
        else:
            raise ParseError('Unknown type declaration: %s' % repr(child))

    def handle_struct(self, proto, name, protoname):
        """Add an ProtocolField to the protocol."""
        subproto = self.all_structs[protoname]
        proto.add_protocol(name, subproto.id, subproto.get_size(), protoname)

    def handle_enum(self, proto, name, enum):
        """Add an EnumField to the protocol."""
        if enum not in self.enums.keys():
            raise ParseError('Unknown enum: %s' % enum)
        type, size = map_type('enum'), size_of('enum')
        proto.add_enum(name, type, size, self.enums[enum])

    def _get_array_size(self, node):
        """Calculate the size of the array."""
        if isinstance(node, c_ast.Constant):
            size = int(node.value)
        elif isinstance(node, c_ast.UnaryOp):
            if node.op == '-':
                size = operator.neg(self._get_array_size(node.expr))
            else:
                size = self._get_array_size(node.expr)
        elif isinstance(node, c_ast.BinaryOp):
            mapping = {'+': operator.add, '-': operator.sub,
                       '*': operator.mul, '/': operator.floordiv}
            left = self._get_array_size(node.left)
            right = self._get_array_size(node.right)
            size = mapping[node.op](left, right)
        elif isinstance(node, c_ast.ID):
            size = 0 # TODO: PATH_MAX?
        else:
            raise ParseError('This type of array not supported: %s' % node)

        return size

    def handle_array_decl(self, node, proto, depth=None):
        """Find member details in an array declaration."""
        if depth is None:
            depth = []
        child = node.children()[0]
        size = self._get_array_size(node.children()[1])

        # String array
        if (isinstance(child, c_ast.TypeDecl) and
                child.children()[0].names[0] == 'char'):
            type = map_type('string')
            size *= size_of('char')
            if depth:
                proto.add_array(child.declname, type, size, depth)
            else:
                self.add_field(proto, child.declname, type, size)
            return

        # Multidimensional, handle recursively
        if isinstance(child, c_ast.ArrayDecl):
            if size > 1:
                depth.append(size)
            self.handle_array_decl(child, proto, depth)

        # Single dimensional normal array
        else:
            depth.append(size)
            ctype = self._get_type(child.children()[0])
            size = size_of(ctype)
            proto.add_array(child.declname, map_type(ctype), size, depth)

    def handle_ptr_decl(self, node, proto):
        """Find member details in a pointer declaration."""
        self.add_field(proto, node.children()[0].declname, 'pointer')

    def add_field(self, proto, name, ctype, size=None):
        """Add a field representing the struct member to the protocol."""
        if size is None:
            try:
                size = size_of(ctype)
            except ValueError :
                size = None # Acceptable if there are rules for the field
        if proto.conf is None:
            if size is None:
                raise ParseError('Unknown size for type %s' % ctype)
            proto.add_field(name, map_type(ctype), size)
        else:
            proto.conf.create_field(proto, name, ctype, size)

