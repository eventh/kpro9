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
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import os
import operator

from pycparser import c_ast, c_parser, plyparser

from config import Options
from platform import Platform
from dissector import Protocol
from field import Field, ArrayField, ProtocolField


class ParseError(plyparser.ParseError):
    """Exception raised by invalid input to the parser."""
    pass


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
    del visitor
    return list(StructVisitor.all_protocols.values())


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    all_protocols = {} # Map struct name to Protocol instances
    all_known_types = {} # Map type name to source filename

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
        # No children, its a member and not a declaration
        if not node.children():
            return

        # Typedef structs
        if not node.name:
            node.name = self.type_decl[-1]

        self._register_type(node) # Register as known type

        # Check if a protocol already exists for this node
        if self._find_protocol(node) is not None:
            return

        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

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

        self._register_type(node) # Register as known type

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

        self._register_type(node) # Register as known type

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
                    return self.handle_array(proto,
                            base[0], base[1], name=node.declname)
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
                hasattr(child.children()[0], 'names') and
                child.children()[0].names[0] == 'char'): #hack
            size *= self.size_of('char')
            return depth, self._create_field(child.declname, 'string', size, 0)

        # Multidimensional, handle recursively
        if isinstance(child, c_ast.ArrayDecl):
            if size > 1:
                depth.append(size)
            return self.handle_array_decl(child, depth)

        # Single dimensional normal array
        depth.append(size)
        sub_child = child.children()[0]

        if isinstance(sub_child, c_ast.IdentifierType):
            ctype = self._get_type(sub_child)

            # Typedef type, which is an alias for another type
            if ctype in self.aliases:
                token, base = self.aliases[ctype]
                if token in ('struct', 'union'):
                    return depth, self._create_protocol_field(
                            child.declname, base)
                elif token == 'enum':
                    return depth, self._create_enum(child.declname, base)
                elif token == 'array':
                    return depth + base[0], base[1]
                else:
                    return depth, self._create_field(child.declname, base)
            else:
                return depth, self._create_field(child.declname, ctype)

        # Enum
        elif isinstance(sub_child, c_ast.Enum):
            return depth, self._create_enum(child.declname, sub_child.name)

        # Union and struct
        elif (isinstance(sub_child, c_ast.Union) or
                isinstance(sub_child, c_ast.Struct)):
            return depth, self._create_protocol_field(
                    child.declname, sub_child.name)

        # Pointer
        elif isinstance(child, c_ast.PtrDecl):
            return depth, self._create_field(sub_child.declname, 'pointer')

        # Error
        else:
            raise ParseError('Unknown type in array: %s' % repr(sub_child))

    def handle_protocol(self, proto, name, proto_name):
        """Add an protocol field or union field to the protocol."""
        return proto.add_field(self._create_protocol_field(name, proto_name))

    def handle_array(self, proto, depth, field, name=None):
        """Add an ArrayField to the protocol."""
        if name is not None:
            field.name = name
        if depth:
            field = ArrayField.create(depth, field)
        return proto.add_field(field)

    def handle_pointer(self, node, proto):
        """Find member details in a pointer declaration."""
        return self.handle_field(proto, node.children()[0].declname, 'pointer')

    def handle_enum(self, proto, name, enum):
        """Add an EnumField to the protocol."""
        return proto.add_field(self._create_enum(name, enum))

    def handle_field(self, proto, name, ctype, size=None, alignment=None):
        """Add a field representing the struct member to the protocol."""
        if alignment is None:
            try:
                alignment = self.alignment(ctype)
            except ValueError :
                alignment = size # Assume that the alignment is the same as the size

        endian = self.platform.endian
        if proto.conf is None:
            if size is None:
                size = self.size_of(ctype)
            if size is None:
                raise ParseError('Unknown alignment for type %s' % ctype)
            return proto.add_field(Field(
                    name, self.map_type(ctype), size, alignment, endian))
        else:
            return proto.conf.create_field(proto, name,
                    ctype, size, alignment, endian)

    def _find_protocol(self, node):
        """Check if the protocol already exists."""
        if node.name not in StructVisitor.all_protocols:
            return None

        # Match platform
        old = StructVisitor.all_protocols[node.name]
        dissector = old.get_dissector(self.platform)
        if dissector is None:
            return None

        # Disallow structs with same name
        if (os.path.normpath(old._file) == os.path.normpath(node.coord.file)
                and old._line == node.coord.line):
            return dissector

        raise ParseError('Two structs with same name %s: %s:%i & %s:%i' % (
               node.name, old._file, old._line,
               node.coord.file, node.coord.line))

    def _create_protocol(self, node, union=False):
        """Create a new protocol for 'node'."""
        conf = Options.configs.get(node.name, None)
        proto, diss = Protocol.create_dissector(
                node.name, self.platform, conf, union=union)

        # Add protocol to list of all protocols
        proto._file = node.coord.file
        proto._line = node.coord.line
        StructVisitor.all_protocols[node.name] = proto
        return diss

    def _create_field(self, name, ctype, size=None, alignment=None):
        if size is None:
            size = self.size_of(ctype)
        if alignment is None:
            alignment = self.alignment(ctype)
        endian = self.platform.endian
        return Field(name, self.map_type(ctype), size, alignment, endian)

    def _create_enum(self, name, enum):
        if enum not in self.enums.keys():
            raise ParseError('Unknown enum: %s' % enum)
        type = self.map_type('enum')
        size = self.size_of('enum')
        alignment = self.alignment('enum')
        field = Field(name, type, size, alignment, self.platform.endian)
        field.set_list_validation(self.enums[enum])
        return field

    def _create_protocol_field(self, name, proto_name):
        proto = StructVisitor.all_protocols.get(proto_name, None)
        if proto is not None:
            proto = proto.get_dissector(self.platform)

        # Try to create a fake protocol if conf has size
        if proto is None:
            conf = Options.config.get(proto_name, None)
            if conf is None or conf.size is None:
                raise ParseError('Unknown protocol %s' % proto_name)
            proto = ProtocolField.Fake(name=proto_name, size=conf.size,
                    alignment=conf.size, endian=self.platform.endian)

        return ProtocolField(name, proto)

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
        else:
            raise ParseError('This type of array not supported: %s' % node)

        return size

    def _register_type(self, node, name=None):
        """Register the type 'name' in the known types mapping."""
        if name is None:
            name = node.name
        StructVisitor.all_known_types[name] = node.coord.file

