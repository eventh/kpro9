"""
TODO
"""

def header(struct):
    protocol = 'local PROTOCOL = Proto ("%s", "struct %s")' % (struct, struct)
    message = 'local luastructs_dt = DissectorTable.get ("luastructs.message")'
    return '%s\n%s\n' % (protocol, message)

def body(struct, members):
    out = ['local f = PROTOCOL.fields']

    for name, type_ in members.items():
        out.append('f.%s = ProtoField.%s ("%s.%s", "%s")' % (
            name, type_, struct, name, name))

    out.append('\nfunction PROTOCOL.dissector (buffer, pinfo, tree)')
    out.append('\tlocal subtree = tree:add (PROTOCOL, buffer())')
    out.append('\tpinfo.cols.info:append (" (" .. PROTOCOL.description .. ")")')
    out.append('')

    for name, type_ in members.items():
        out.append('\tsubtree:add (f.%s, buffer(0,0))' % name)

    out.append('end\n\nluastructs_dt:add (1, PROTOCOL)\n')

    return '\n'.join(out)

def generate(struct, members=None):
    if members is None:
        members = {}
    return '%s\n%s' % (header(struct), body(struct, members))

def create(filename, *args, **vargs):
    with open(filename, 'w') as f:
        f.write(generate(*args, **vargs))

