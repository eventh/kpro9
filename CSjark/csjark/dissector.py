"""
A module for generating LUA dissectors for Wireshark.
"""

#INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
#OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
#                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
#VALID_PROTOTYPES = INT_TYPES + OTHER_TYPES


def _dict_to_table(pydict):
    """Convert a python dictionary to lua table."""
    return '{%s}' % ', '.join('[%i]="%s"' % (i, j) for i, j in pydict.items())


class Field:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size
        self.protocol = None

    def get_definition(self):
        """Get the ProtoField definition for this field."""
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


class EnumField(Field):
    def __init__(self, name, type, size, values, strict=True):
        super().__init__(name, type, size)
        self.values = values
        self.strict = strict

        # The func to call to get the value from the buffer
        self.func_type = self.type
        if self.func_type[-2:] in ('16', '32'):
            self.func_type = self.func_type[:-2]

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        t = '{var}.{name} = ProtoField.{type}("{protocol}.{name}", "{name}"' \
                ', nil, {values})'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'protocol': self.protocol.name, 'type': self.type,
                'values': _dict_to_table(self.values)}
        return t.format(**args)

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        t = '\tlocal {name} = subtree:add({var}.{name}, buffer({offset}, {size}))'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'offset': offset, 'size': self.size}
        data.append(t.format(**args))

        # Test that the enum value is valid
        if self.strict:
            data.append('\tlocal test = %s' % _dict_to_table(self.values))
            data.append('\tif (test[buffer(%i, %i):%s()] == nil) then' % (
                    offset, self.size, self.func_type))
            warn = 'Invalid value, not in (%s)' % ', '.join(
                    str(i) for i in sorted(self.values.keys()))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, "%s")'
                    % (self.name, warn))
            data.append('\tend')

        return '\n'.join(data)

class RangeField(Field):
    def __init__(self, name, type, size, min, max):
        super().__init__(name, type, size)
        self.min = min
        self.max = max

        # The func to call to get the value from the buffer
        self.func_type = self.type
        if self.func_type[-2:] in ('16', '32'):
            self.func_type = self.func_type[:-2]

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
            data.append('\tif (buffer(%i, %i):%s() %s %s) then' %
                    (offset, self.size, self.func_type, test, value))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, '
                            '"Should be %s %s")' % (self.name, warn, value))
            data.append('\tend')

        if self.min is not None:
            create_test(self.min, '<', 'larger than')
        if self.max is not None:
            create_test(self.max, '>', 'smaller than')

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

