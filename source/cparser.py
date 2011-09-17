#! /usr/bin/env python
"""
A module for parsing C files, and searching AST for struct definitions.

Requires PLY and pycparser.
"""
import sys
import pycparser
from pycparser import c_ast, c_parser


def parse_file(filename, use_cpp=True, fake_includes=True, cpp_args=None):
    """Parse a C file, returns abstract syntax tree.

    use_cpp: Enable or disable the C preprocessor
    fake_includes: Add fake includes for libc header files
    cpp_args: Provide additional arguments for the C preprocessor
    """
    cpp_path = 'cpp'

    if use_cpp:
        if cpp_args is None:
            cpp_args = []
        if fake_includes:
            cpp_args.append(r'-I/utils/fake_libc_include')

        if sys.platform == 'win32':
            cpp_path = './utils/cpp.exe' # Windows don't come with a CPP
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


class CStruct:
    def __init__(self, name, members):
        self.name = name
        self.members = members


class CStructMember:
    def __init__(self, name, ctype, type, size):
        self.name = name
        self.ctype = ctype
        self.type = type
        self.size = size


# Mapping of c type and their default size in bytes.
C_SIZE_MAP = {
        'bool': 1,
        'char': 1,
        'signed char': 1,
        'unsigned char': 1,
        'short': 2,
        'short int': 2,
        'signed short int': 2,
        'unsigned short int': 2,
        'int': 4,
        'signed int': 4,
        'unsigned int': 4,
        'long': 8,
        'long int': 8,
        'signed long int': 8,
        'unsigned long int': 8,
        'long long': 8,
        'long long int': 8,
        'signed long long int': 8,
        'unsigned long long int': 8,
        'float': 4,
        'double': 8,
        'long double': 16,
        'pointer': 4,
}


def _size_of(ctype):
    if ctype in C_SIZE_MAP.keys():
        return C_SIZE_MAP[ctype]

    if ctype == 'enum':
        return 7
    elif ctype == 'array':
        return 13
    else:
        return 1


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    def __init__(self):
        self.structs = []

    def visit_Struct(self, node):
        """Visit a Struct node in the AST."""
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # Find the member definitions
        members = []
        for decl in node.children():
            child = decl.children()[0]

            if isinstance(child, c_ast.TypeDecl):
                members.append(self.handle_type_decl(child))
            elif isinstance(child, c_ast.ArrayDecl):
                members.append(self.handle_array_decl(child))
            elif isinstance(child, c_ast.PtrDecl):
                members.append(self.handle_ptr_decl(child))
            else:
                raise Exception("Unknown struct member type")

        # Create the struct
        struct = CStruct(node.name, members)
        self.structs.append(struct)

    def handle_type_decl(self, node):
        """Find member details in a type declaration."""
        child = node.children()[0]
        if isinstance(child, c_ast.IdentifierType):
            ctype = ' '.join(reversed(child.names))
            type = child.names[0]
        elif isinstance(child, c_ast.Enum):
            ctype = "enum"
            type = "enum"
        elif isinstance(child, c_ast.Union):
            ctype = "union"
            type = "union"

        return CStructMember(node.declname, ctype, type, _size_of(ctype))

    def handle_array_decl(self, node):
        """Find member details in an array declaration."""
        type_decl, constant = node.children()
        child = self.handle_type_decl(type_decl)

        ctype = child.ctype
        type = child.type
        size = int(constant.value) * _size_of(child.size)

        return CStructMember(type_decl.declname, ctype, type, size)

    def handle_ptr_decl(self, node):
        """Find member details in a pointer declaration."""
        type_decl = node.children()[0]
        ctype = type = 'pointer' # Shortcut as pointers not a requirement
        size = _size_of(ctype)
        return CStructMember(type_decl.declname, ctype, type, size)


def find_structs(ast):
    """Walks the AST nodes to find structs."""
    visitor = StructVisitor()
    visitor.visit(ast)
    return visitor.structs


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ast = parse(sys.argv[1])
        ast.show()
    else:
        print("Please provide a C file to parse")

