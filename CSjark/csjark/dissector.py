"""
A module for generating LUA dissectors for Wireshark.
"""

INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
VALID_PROTOTYPES = INT_TYPES + OTHER_TYPES


class Field:
    def __init__(self, name, type, size, protocol=None):
        self.name = name
        self.type = type
        self.size = size
        self.protocol = protocol

    def get_def_extra(self):
        """Overload to add extra code above field definition."""
        return []

    def get_definition(self):
        """Get the ProtoField definition for this Field."""
        t = '{var}.{name} = ProtoField.{type}("{protocol}.{name}", "{name}")'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'protocol': self.protocol.name, 'type': self.type}

        data = self.get_def_extra()
        data.append(t.format(**args))
        return '\n'.join(data)

    def get_code_extra(self):
        """Overload to add extra code above the field code."""
        return []

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        t = '\tsubtree:add ({var}.{name}, buffer({offset},{size}))'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'offset': offset, 'size': self.size}

        data = self.get_code_extra()
        data.append(t.format(**args))
        return '\n'.join(data)


class IntRange(Field):
    pass


class Protocol:
    counter = 0

    def __init__(self, name, fields=None, id=None):
        self.name = name

        if fields is None:
            fields = []
        self.fields = fields

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

    def add_fields(self):
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))
        self.data.extend([f.get_definition() for f in self.fields])
        self.data.append('')

    def add_dissector(self):
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:add({var}, buffer())'
        desc = '\tpinfo.cols.info:append(" (" .. {var}.description .. ")")'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(var=self.var))
        self.data.append(desc.format(var=self.var))
        self.data.append('')

        offset = 0
        for field in self.fields:
            self.data.append(field.get_code(offset))
            offset += field.size

        self.data.append('end')
        self.data.append('')

    def create(self):
        for field in self.fields:
            field.protocol = self # Temp hack

        self.add_header()
        self.add_fields()
        self.add_dissector()

        end = 'luastructs_dt:add({id}, {var})\n'
        self.data.append(end.format(id=self.id, var=self.var))

        return '\n'.join(self.data)

