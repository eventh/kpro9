"""
A module for generating LUA dissectors for Wireshark.
"""

LUA_TYPES = {
        "int": "uint32",
        "array": "string",
}

def map_type(c_type):
    return LUA_TYPES.get(c_type, c_type)

def header(struct):
    name = struct.name
    protocol = 'local PROTOCOL = Proto ("%s", "struct %s")' % (name, name)
    message = 'local luastructs_dt = DissectorTable.get ("luastructs.message")'
    return '%s\n%s\n' % (protocol, message)

def body(struct):
    out = ['local f = PROTOCOL.fields']

    for member in struct.members:
        out.append('f.%s = ProtoField.%s ("%s.%s", "%s")' % (
            member.name, map_type(member.type_),
            struct.name, member.name, member.name))

    out.append('\nfunction PROTOCOL.dissector (buffer, pinfo, tree)')
    out.append('\tlocal subtree = tree:add (PROTOCOL, buffer())')
    out.append('\tpinfo.cols.info:append (" (" .. PROTOCOL.description .. ")")')
    out.append('')

    for member in struct.members:
        out.append('\tsubtree:add (f.%s, buffer(0,0))' % member.name)

    out.append('end\n\nluastructs_dt:add (1, PROTOCOL)\n')

    return '\n'.join(out)


def generate(struct):
    return '%s\n%s\n' % (header(struct), body(struct))


def write(structs):
    for struct in structs:
        with open('%s.lua' % struct.name, 'w') as f:
            f.write(generate(struct))

