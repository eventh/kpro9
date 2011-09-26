#! /usr/bin/env python
"""
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import sys
import pycparser
from pycparser import c_ast, c_parser
from config import DEFAULT_C_SIZE_MAP, DEFAULT_C_TYPE_MAP, StructConfig
from dissector import Protocol, Field


def parse_file(filename, use_cpp=True,
        fake_includes=True, cpp_args=None, cpp_path=None):
    """Parse a C file, returns abstract syntax tree.

    use_cpp: Enable or disable the C preprocessor
    fake_includes: Add fake includes for libc header files
    cpp_args: Provide additional arguments for the C preprocessor
    cpp_path: The path to cpp.exe on windows
    """
    if cpp_path is None:
        cpp_path = 'cpp'

    if use_cpp:
        if cpp_args is None:
            cpp_args = []
        if fake_includes:
            cpp_args.append(r'-I../utils/fake_libc_include')

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

        # Create the protocol for the struct
        proto = Protocol(node.name)
        self.structs.append(proto)

        # Find config rules
        conf = StructConfig.configs.get(node.name, None)

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
                raise Exception("Unknown struct member type")

    def handle_type_decl(self, node, proto, conf):
        """Find member details in a type declaration."""
        child = node.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            ctype = ' '.join(reversed(child.names))
        elif isinstance(child, c_ast.Enum):
            ctype = "enum"
        elif isinstance(child, c_ast.Union):
            ctype = "union"
        self._create_field(proto, conf, node.declname, ctype)

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
            raise Exception('array of different types not supported yet.')

        size = int(constant.value) * self._size_of(ctype)
        self._create_field(proto, conf, type_decl.declname, ctype, size=size)

    def handle_ptr_decl(self, node, proto, conf):
        """Find member details in a pointer declaration."""
        type_decl = node.children()[0]
        ctype = 'pointer' # Shortcut as pointers not a requirement
        self._create_field(proto, conf, type_decl.declname, ctype)

    def _create_field(self, proto, conf, name, ctype, size=None):
        """Create a dissector field representing the struct member."""
        # Find all rules relevant for this field
        if conf is not None:
            rules = conf.get_rules(name, ctype)

        # Map from C to wireshark values
        type_ = self._map_type(ctype)
        if size is None:
            size = self._size_of(ctype)

        proto.add_field(Field(name, type_, size))

    def _map_type(self, ctype):
        """Find the wireshark type for a ctype."""
        return DEFAULT_C_TYPE_MAP.get(ctype, ctype)

    def _size_of(self, ctype):
        """Find the size of a c type in bytes."""
        if ctype in DEFAULT_C_SIZE_MAP.keys():
            return DEFAULT_C_SIZE_MAP[ctype]
        else:
            return 1


def find_structs(ast):
    """Walks the AST nodes to find structs."""
    visitor = StructVisitor()
    visitor.visit(ast)
    return visitor.structs


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ast = parse_file(sys.argv[1])
        ast.show()
    else:
        print("Please provide a C file to parse")

