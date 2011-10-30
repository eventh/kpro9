"""
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import sys
import os
import operator

import pycparser
from pycparser import c_ast, c_parser, plyparser

from config import Options
from platform import Platform
from dissector import Protocol, UnionProtocol


class ParseError(plyparser.ParseError):
    """Exception raised by invalid input to the parser."""
    pass


def parse_file(filename, platform=None):
    """Parse a C file, returns abstract syntax tree."""
    file = filename
    cpp_path = 'cpp'

    if Options.use_cpp:
        cpp_args = []

        cpp_args.append(r'-I../utils/fake_libc_include')
        cpp_args.extend(Options.cpp_includes)

        if os.path.dirname(filename):
            cpp_args.append(r'-I%s' % os.path.dirname(filename))

        if sys.platform == 'win32' and cpp_path == 'cpp':
            cpp_path = '../utils/cpp.exe' # Windows don't come with a CPP
        elif sys.platform == 'darwin':
            cpp_path = 'gcc' # Fix for a bug in Mac GCC 4.2.1
            cpp_args.append('-E')

        # Create temporary header with platform-specific macros
        if platform is not None:
            file = 'temp-%s.tmp.h' % os.path.split(filename)[1]
            with open(file, 'w') as fp:
                fp.write('%s#include "%s"\n\n' % (platform.header, filename))
    else:
        cpp_args = None

    # Generate an abstract syntax tree
    ast = pycparser.parse_file(file, use_cpp=Options.use_cpp,
                               cpp_path=cpp_path, cpp_args=cpp_args)

    # Delete temp file, can't use real tempfile as we call CPP program
    if file != filename:
        os.remove(file)

    return ast


def parse(text, filename=''):
    """Parse C code and return an AST."""
    parser = c_parser.CParser()
    return parser.parse(text, filename)


def find_structs(ast, platform=None):
    """Walks the AST nodes to find structs."""
    if platform is None:
        platform = Platform.mappings['default']

    visitor = StructVisitor(platform)
    visitor.visit(ast)
    return list(StructVisitor.all_protocols.values())


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    all_protocols = {}

    def __init__(self, platform):
        """Create a new instance to visit all nodes in the AST.

        'platform' is the platform the header was parsed for
        """
        self.platform = platform
        self.map_type = platform.map_type
        self.size_of = platform.size_of
        self.alignment = platform.alignment_size_of

        self.enums = {} # All enums encountered in this AST
        self.aliases = {} # Typedefs and their base type
        self.type_decl = [] # Queue of current type declaration

    def visit_Struct(self, node):
        """Visit a Struct node in the AST."""
        self._visit_nodes(node)

    def visit_Union(self, node):
        """Visit a Union node in the AST."""
        self._visit_nodes(node, union=True)

    def _visit_nodes(self, node, union=False):
        """Visit a node in the tree."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # No children, its a member and not a declaration
        if not node.children():
            return

        # Typedef structs
        if not node.name:
            node.name = self.type_decl[-1]

        # Create the protocol for the struct
        proto = self._create_protocol(node, union)
        if proto is None:
            return # We have already created this protocol

        # Find the member definitions
        for decl in node.children():
            child = decl.children()[0]

            if isinstance(child, c_ast.TypeDecl):
                self.handle_type_decl(child, proto)
            elif isinstance(child, c_ast.ArrayDecl):
                self.handle_array(proto, *self.handle_array_decl(child))
            elif isinstance(child, c_ast.PtrDecl):
                self.handle_pointer(child, proto)
            else:
                raise ParseError('Unknown struct member: %s' % repr(child))

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
            self.aliases[node.name] = self.aliases.get(ctype, (None, ctype))
        elif isinstance(child, c_ast.Enum):
            self.aliases[node.name] = ('enum', child.name)
        elif isinstance(child, c_ast.Struct):
            self.aliases[node.name] = ('struct', child.name)
        elif isinstance(child, c_ast.Union):
            self.aliases[node.name] = ('union', child.name)
        elif isinstance(node.children()[0], c_ast.ArrayDecl):
            values = self.handle_array_decl(node.children()[0])
            self.aliases[node.name] = ('array', values)
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
                token, base = self.aliases[ctype]
                if token in ('struct', 'union'):
                    return self.handle_protocol(proto, node.declname, base)
                elif token == 'enum':
                    return self.handle_enum(proto, node.declname, base)
                elif token == 'array':
                    tmp, ctype, size, alignment, depth = base
                    return self.handle_array(proto, node.declname,
                                             ctype, size, alignment, depth)
                else:
                    # If any rules exists, use new type and not base
                    if proto.conf and proto.conf.get_rules(None, ctype):
                        base = ctype # Is this wise?
                    return self.handle_field(proto, node.declname, base)
            else:
                return self.handle_field(proto, node.declname, ctype)

        # Enum member
        elif isinstance(child, c_ast.Enum):
            return self.handle_enum(proto, node.declname, child.name)
        # Union member
        elif isinstance(child, c_ast.Union):
            return self.handle_protocol(proto, node.declname, child.name)
        # Struct member
        elif isinstance(child, c_ast.Struct):
            return self.handle_protocol(proto, node.declname, child.name)
        # Error
        else:
            raise ParseError('Unknown type declaration: %s' % repr(child))

    def handle_array_decl(self, node, depth=None):
        """Find the depth and size of the array."""
        if depth is None:
            depth = []
        child = node.children()[0]
        size = self._get_array_size(node.children()[1])

        # String array
        if (isinstance(child, c_ast.TypeDecl) and
                hasattr(child.children()[0], 'names') and child.children()[0].names[0] == 'char'): #hack
            size *= self.size_of('char')
            return child.declname, 'string', size, self.alignment('char'), depth

        # Multidimensional, handle recursively
        if isinstance(child, c_ast.ArrayDecl):
            if size > 1:
                depth.append(size)
            return self.handle_array_decl(child, depth)

        # Single dimensional normal array
        depth.append(size)
        
        if isinstance(child.children()[0], c_ast.IdentifierType):
            ctype = self._get_type(child.children()[0])

            # Typedef type, which is an alias for another type
            if ctype in self.aliases:
                token, base = self.aliases[ctype]
                if token in ('struct', 'union'):
                    subproto = self.all_protocols[base, self.platform]
                    return child.declname, subproto, subproto.get_size(), subproto.get_alignment_size(), depth
                elif token == 'enum':
                    return child.declname, token, self.size_of(token), self.alignment(token), depth, self.enums[ctype]
                elif token == 'array':
                    tmp, ctype, size, alignment, inner_depth = base
                    return child.declname, ctype, size, alignment, depth + inner_depth
                else:
                    base_size = self.size_of(base)
                    base_alignment_size = self.alignment(base)
                    return child.declname, base, base_size, base_alignment_size, depth
            else:
                base_size = self.size_of(ctype)
                base_alignment_size = self.alignment(ctype)
                return child.declname, ctype, base_size, base_alignment_size, depth
        # Enum
        elif isinstance(child.children()[0], c_ast.Enum):
            return child.declname, 'enum', self.size_of('enum'), self.alignment('enum'), depth, self.enums[child.children()[0].name]
        # Union and struct
        elif isinstance(child.children()[0], c_ast.Union) or isinstance(child.children()[0], c_ast.Struct):
            subproto = self.all_protocols[child.children()[0].name, self.platform]
            return child.declname, subproto, subproto.get_size(), subproto.get_alignment_size(), depth
        # Error
        else:
            
            raise ParseError('Unknown type in array declaration: %s' % repr(child.children()[0]))

    def handle_protocol(self, proto, name, proto_name):
        """Add an protocol field or union field to the protocol."""
        sub_proto = StructVisitor.all_protocols[(proto_name, self.platform)]
        return proto.add_protocol(name, sub_proto)

    def handle_array(self, proto, name, ctype, size, alignment, depth, enum_members = None):
        """Add an ArrayField to the protocol."""
        if not depth:
            return self.handle_field(proto, name, ctype, size, alignment)
        
        return proto.add_array(name, ctype, size, alignment, depth, enum_members)

    def handle_pointer(self, node, proto):
        """Find member details in a pointer declaration."""
        return self.handle_field(proto, node.children()[0].declname, 'pointer')

    def handle_enum(self, proto, name, enum):
        """Add an EnumField to the protocol."""
        if enum not in self.enums.keys():
            raise ParseError('Unknown enum: %s' % enum)

        type = self.map_type('enum')
        size = self.size_of('enum')
        alignment = self.alignment('enum')

        return proto.add_enum(name, type, size, alignment, self.enums[enum])

    def handle_field(self, proto, name, ctype, size=None, alignment=None):
        """Add a field representing the struct member to the protocol."""
        if alignment is None:
            try:
                alignment = self.alignment(ctype)
            except ValueError :
                alignment = size # Assume that the alignment is the same as the size

        if proto.conf is None:
            if size is None:
                size = self.size_of(ctype)
            if size is None:
                raise ParseError('Unknown alignment for type %s' % ctype)
            return proto.add_field(name, self.map_type(ctype), size, alignment)
        else:
            return proto.conf.create_field(proto, name, ctype, size, alignment)

    def _create_protocol(self, node, union=False):
        """Create a new protocol for 'node'."""
        conf = Options.configs.get(node.name, None)
        if union:
            proto = UnionProtocol(node.name, conf, self.platform)
        else:
            proto = Protocol(node.name, conf, self.platform)
        proto._coord = node.coord

        return self._store_protocol(node, proto)

    def _store_protocol(self, node, proto):
        """Store the protocol, unless it already exists."""
        # Add protocol to list of all protocols
        if (node.name, self.platform) not in StructVisitor.all_protocols:
            StructVisitor.all_protocols[(node.name, self.platform)] = proto
            return proto

        old_proto = StructVisitor.all_protocols[(node.name, self.platform)]

        # Don't re-create already created protocols
        o, norm = old_proto._coord, os.path.normpath
        if norm(o.file) == norm(node.coord.file) and o.line == node.coord.line:
            del proto
            return None

        # Disallow structs with same name
        raise ParseError('Two structs with same name %s: %s:%i & %s:%i' % (
               node.name, o.file, o.line, node.coord.file, node.coord.line))

    def _get_type(self, node):
        """Get the C type from a node."""
        return ' '.join(reversed(node.names))

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

