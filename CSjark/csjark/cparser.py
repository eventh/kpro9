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
from dissector import Protocol


class ParseError(plyparser.ParseError):
    """Exception raised by invalid input to the parser."""
    pass


def parse_file(filename):
    """Parse a C file, returns abstract syntax tree."""
    cpp_path = 'cpp'

    if Options.use_cpp:
        cpp_args = []

        cpp_args.append(r'-I../utils/fake_libc_include')

        if os.path.dirname(filename):
            cpp_args.append(r'-I%s' % os.path.dirname(filename))

        if sys.platform == 'win32' and cpp_path == 'cpp':
            cpp_path = '../utils/cpp.exe' # Windows don't come with a CPP
        elif sys.platform == 'darwin':
            cpp_path = 'gcc' # Fix for a bug in Mac GCC 4.2.1
            cpp_args.append('-E')
    else:
        cpp_args = None

    # Generate an abstract syntax tree
    ast = pycparser.parse_file(filename, use_cpp=Options.use_cpp,
                               cpp_path=cpp_path, cpp_args=cpp_args)
    return ast


def parse(text, filename=''):
    """Parse C code and return an AST."""
    parser = c_parser.CParser()
    return parser.parse(text, filename)


def find_structs(ast, platform=None):
    """Walks the AST nodes to find structs."""
    if platform is None:
        platform = Platform.mappings[''] # Use default platform
    visitor = StructVisitor(platform)
    visitor.visit(ast)
    return visitor.structs


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    all_structs = {} # Map struct names and their protocol

    def __init__(self, platform):
        self.platform = platform
        self.map_type = platform.map_type
        self.size_of = platform.size_of

        self.structs = [] # All structs encountered in this AST
        self.enums = {} # All enums encountered in this AST
        self.aliases = {} # Typedefs and their base type
        self.type_decl = [] # Queue of current type declaration

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
        proto = self._create_protocol(node)

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
                if token == 'enum':
                    return self.handle_enum(proto, node.declname, base)
                elif token == 'struct':
                    return self.handle_struct(proto, node.declname, base)
                elif token == 'array':
                    tmp, ctype, size, depth = base
                    return self.handle_array(proto, node.declname,
                                             ctype, size, depth)
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
            return self.handle_field(proto, node.declname, 'union')
        # Struct member
        elif isinstance(child, c_ast.Struct):
            return self.handle_struct(proto, node.declname, child.name)
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
                child.children()[0].names[0] == 'char'):
            size *= self.size_of('char')
            return child.declname, 'string', size, depth

        # Multidimensional, handle recursively
        if isinstance(child, c_ast.ArrayDecl):
            if size > 1:
                depth.append(size)
            return self.handle_array_decl(child, depth)

        # Single dimensional normal array
        depth.append(size)
        ctype = self._get_type(child.children()[0])

        # Support for typedef
        if ctype in self.aliases:
            token, ctype = self.aliases[ctype]
            if token is not None:
                print(token, ctype) # TODO
                raise ParseError('Incomplete support for array of typedefs')

        return child.declname, ctype, self.size_of(ctype), depth

    def handle_union_decl(self, node):
        """Find the members and size of an union."""
        pass

    def handle_union(self, proto, name, members):
        """Add an UnionField to the protocol."""
        pass

    def handle_array(self, proto, name, ctype, size, depth):
        """Add an ArrayField to the protocol."""
        if not depth:
            return self.handle_field(proto, name, ctype, size)
        return proto.add_array(name, self.map_type(ctype), size, depth)

    def handle_pointer(self, node, proto):
        """Find member details in a pointer declaration."""
        return self.handle_field(proto, node.children()[0].declname, 'pointer')

    def handle_struct(self, proto, name, protoname):
        """Add an ProtocolField to the protocol."""
        subproto = self.all_structs[protoname]
        return proto.add_protocol(name,
                    subproto.id, subproto.get_size(), protoname)

    def handle_enum(self, proto, name, enum):
        """Add an EnumField to the protocol."""
        if enum not in self.enums.keys():
            raise ParseError('Unknown enum: %s' % enum)
        type, size = self.map_type('enum'), self.size_of('enum')
        return proto.add_enum(name, type, size, self.enums[enum])

    def handle_field(self, proto, name, ctype, size=None):
        """Add a field representing the struct member to the protocol."""
        if size is None:
            try:
                size = self.size_of(ctype)
            except ValueError :
                size = None # Acceptable if there are rules for the field
        if proto.conf is None:
            if size is None:
                raise ParseError('Unknown size for type %s' % ctype)
            return proto.add_field(name, self.map_type(ctype), size)
        else:
            return proto.conf.create_field(proto, name, ctype, size)

    def _create_protocol(self, node):
        """Create a new protocol for 'node'."""
        conf = Options.configs.get(node.name, None)
        proto = Protocol(node.name, conf, self.platform)
        proto._coord = node.coord

        # Disallow structs with same name
        if node.name in StructVisitor.all_structs:
            o = StructVisitor.all_structs[node.name]._coord
            if (os.path.normpath(o.file) != os.path.normpath(node.coord.file)
                    or o.line != node.coord.line):
                raise ParseError('Two structs with same name %s: %s:%i & %s:%i' % (
                       node.name, o.file, o.line, node.coord.file, node.coord.line))

        # Add struct to list of all structs
        self.structs.append(proto)
        self.all_structs[node.name] = proto

        return proto

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

