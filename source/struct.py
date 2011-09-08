"""
A module for searching an AST for structs.

Also contains the Struct and its members data types.
"""
from pycparser import c_ast


class Struct:
    def __init__(self, name, members):
        self.name = name
        self.members = members


class Member:
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_


class StructVisitor(c_ast.NodeVisitor):
    """A class which visit struct nodes in the AST."""

    def __init__(self):
        self.structs = []

    def visit_Struct(self, node):
        # Visit children
        c_ast.NodeVisitor.generic_visit(self, node)

        # Find the member values
        members = []
        for child in node.children():
            if not isinstance(child, c_ast.Decl):
                raise Exception("invalid struct member")
            members.append(self.handle_Member(child))

        # Create the struct
        struct = Struct(node.name, members)
        self.structs.append(struct)

    def handle_Member(self, node):
        child = node.children()[0]
        if isinstance(child, c_ast.TypeDecl):
            type_ = ' '.join(child.type.names)
        elif isinstance(child, c_ast.ArrayDecl):
            type_ = "array"
        else:
            type_ = "unknown"

        return Member(node.name, type_)


def find_structs(ast):
    """Walks the AST nodes to find structs."""
    visitor = StructVisitor()
    visitor.visit(ast)
    return visitor.structs

