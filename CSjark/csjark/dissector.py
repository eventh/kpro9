"""
A module for generating LUA dissectors for Wireshark.
"""

INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
VALID_PROTOTYPES = INT_TYPES + OTHER_TYPES


class Field:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size
        self.protocol = None

    def get_definition(self):
        """Get the ProtoField definition for this Field."""
        t = '{var}.{name} = ProtoField.{type}("{protocol}.{name}", "{name}")'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'protocol': self.protocol.name, 'type': self.type}
        return t.format(**args)

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        t = '\tsubtree:add({var}.{name}, buffer({offset}, {size}))'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'offset': offset, 'size': self.size,}
        return t.format(**args)


class RangeField(Field):
    def __init__(self, min, max, *args, **vargs):
        super().__init__(*args, **vargs)
        self.min = min
        self.max = max

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        t = '\tlocal {name} = subtree:add({var}.{name}, buffer({offset}, {size}))'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'offset': offset, 'size': self.size}

        data.append(t.format(**args))

        # Test the value
        def create_test(value, test, warn):
            type_ = self.type
            if type_[-2:] in ('16', '32'):
                type_ = type_[:-2]
            data.append('\tlocal %s_val = buffer(%i, %i):%s()' % (
                            self.name, offset, self.size, type_))
            data.append('\tif (%s %s %s_val) then' % (value, test, self.name))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, '
                            '"Should be %s %s")' % (self.name, warn, value))
            data.append('\tend')

        if self.min is not None:
            create_test(self.min, '>', 'larger than')
        if self.max is not None:
            create_test(self.max, '<', 'smaller than')

        return '\n'.join(data)


class Protocol:
    counter = 0

    def __init__(self, name, id=None, description=None):
        self.name = name

        if id is None:
            Protocol.counter += 1
            self.id = Protocol.counter
        else:
            self.id = id

        if description is None:
            self.description = 'struct %s' % self.name
        else:
            self.description = description

        self.fields = []
        self.data = []
        self.var = 'proto_{name}'.format(name=self.name)
        self.field_var = 'f'
        self.dissector = 'luastructs.message'

    def add_field(self, field):
        """Add a field to the dissector, updates the fields protocol."""
        field.protocol = self
        self.fields.append(field)

    def _header_defintion(self):
        proto = 'local {var} = Proto("{name}", "{description}")'
        table = 'local luastructs_dt = DissectorTable.get("{dissector}")'

        self.data.append(proto.format(var=self.var,
                         name=self.name, description=self.description))
        self.data.append(table.format(dissector=self.dissector))
        self.data.append('')

    def _fields_definition(self):
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))
        self.data.extend([f.get_definition() for f in self.fields])
        self.data.append('')

    def _dissector_func(self):
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
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()

        end = 'luastructs_dt:add({id}, {var})\n'
        self.data.append(end.format(id=self.id, var=self.var))

        return '\n'.join(self.data)

