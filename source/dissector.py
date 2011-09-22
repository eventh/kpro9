"""
A module for generating LUA dissectors for Wireshark.
"""

LUA_TYPES = {
        "int": "uint32",
        "array": "string",
}

def map_type(c_type):
    return LUA_TYPES.get(c_type, c_type)


class Field:
    def __init__(self, name, type, size, var='f'):
        self.name = name
        self.type = type
        self.size = size
        self.var = var

    def get_def_extra(self):
        """Overload to add extra code above field definition."""
        return []

    def get_definition(self, struct):
        """Get the ProtoField definition for this Field."""
        t = '{var}.{name} = ProtoField.{type}("{struct}.{name}", "{name}")'
        args = {'var': self.var, 'struct': struct,
                'name': self.name, 'type': self.type}

        data = self.get_def_extra()
        data.append(t.format(**args))
        return '\n'.join(data)

    def get_code_extra(self):
        """Overload to add extra code above the field code."""
        return []

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        t = '\tsubtree:add ({var}.{name}, buffer({offset},{size}))'
        args = {'var': self.var, 'name': self.name,
                'offset': offset, 'size': self.size}

        data = self.get_code_extra()
        data.append(t.format(**args))
        return '\n'.join(data)


class IntRange(Field):
    pass


class Protocol:
    counter = 0

    def __init__(self, name, id=None):
        self.name = name
        if id is None:
            Protocol.counter += 1
            self.id = Protocol.counter
        else:
            self.id = id

        self.var = 'proto_{name}'.format(name=self.name)
        self.field_var = 'f'
        self.dissector = 'luastructs.message'

        self.data = []

    def add_header(self):
        proto = 'local {var} = Proto("{name}", "struct {name}")'
        table = 'local luastructs_dt = DissectorTable.get("{dissector}")'

        self.data.append(proto.format(var=self.var, name=self.name))
        self.data.append(table.format(dissector=self.dissector))
        self.data.append('')

    def add_fields(self, members):
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))

        for member in members:
            self.data.append(member.field.get_definition(self.name))

        self.data.append('')

    def add_dissector(self, members):
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:add({var}, buffer())'
        desc = '\tpinfo.cols.info:append(" (" .. {var}.description .. ")")'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(var=self.var))
        self.data.append(desc.format(var=self.var))

        offset = 0
        for member in members:
            self.data.append(member.field.get_code(offset))
            offset += member.field.size

        self.data.append('end')
        self.data.append('')

    def create(self, struct):
        # Temp create field
        for m in struct.members:
            m.field = Field(m.name, map_type(m.type), m.size, self.field_var)

        self.add_header()
        self.add_fields(struct.members)
        self.add_dissector(struct.members)

        end = 'luastructs_dt:add({id}, {var})\n'
        self.data.append(end.format(id=self.id, var=self.var))

        return '\n'.join(self.data)

