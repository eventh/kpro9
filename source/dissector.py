"""
A module for generating LUA dissectors for Wireshark.
"""

LUA_TYPES = {
        "int": "uint32",
        "array": "string",
}

def map_type(c_type):
    return LUA_TYPES.get(c_type, c_type)


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
        self.dissector = 'luastructs.message'

        self.data = []

    def add_header(self):
        proto = 'local {var} = Proto("{name}", "struct {name}")'
        table = 'local luastructs_dt = DissectorTable.get("{dissector}")'

        self.data.append(proto.format(var=self.var, name=self.name))
        self.data.append(table.format(dissector=self.dissector))
        self.data.append('')

    def add_dissector(self, struct):
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:add({var}, buffer())'
        desc = '\tpinfo.cols.info:append(" (" .. {var}.description .. ")")'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(var=self.var))
        self.data.append(desc.format(var=self.var))

        offset = 0
        for member in struct.members:
            self.data.append('\tsubtree:add (f.%s, buffer(%i,%i))' % (
                                    member.name,offset, member.size))
            offset += member.size

        self.data.append('end')
        self.data.append('')

    def add_fields(self, struct):
        decl = 'local f = {var}.fields'
        self.data.append(decl.format(var=self.var))

        for member in struct.members:
            self.data.append('f.%s = ProtoField.%s("%s.%s", "%s")' % (
                member.name, map_type(member.type),
                struct.name, member.name, member.name))

        self.data.append('')

    def create(self, struct):
        self.add_header()
        self.add_fields(struct)
        self.add_dissector(struct)

        end = 'luastructs_dt:add({id}, {var})\n'
        self.data.append(end.format(id=self.id, var=self.var))

        return '\n'.join(self.data)

