"""
A module for generating LUA dissectors for Wireshark.
"""

#INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
#OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
#                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
#VALID_PROTOTYPES = INT_TYPES + OTHER_TYPES


class Field:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

        self.base = None # One of 'base.DEC', 'base.HEX' or 'base.OCT'
        self.values = None # Dict with the text that corresponds to the values
        self.mask = None # Integer mask of this field
        self.desc = None # Description of the field

        self.protocol = None # The protocol which owns the field

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        var = self.protocol.field_var
        abbr = '%s.%s' % (self.protocol.name, self.name)

        # Create definition string
        t = '{var}.{name} = ProtoField.{type}("{abbr}", "{name}"'.format(
                var=var, name=self.name, abbr=abbr, type=self.type)

        # Add other parameters if applicable
        rest = []
        for var in reversed([self.base, self.values, self.mask, self.desc]):
            if rest or var is not None:
                if var is None:
                    var = 'nil'
                rest.append(var)
        if rest:
            rest.append('')

        return '%s%s)' % (t, ', '.join(reversed(rest)))

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        t = '\tsubtree:add({var}.{name}, buffer({offset}, {size}))'
        args = {'var': self.protocol.field_var, 'name': self.name,
                'offset': offset, 'size': self.size,}
        return t.format(**args)

    def _get_func_type(self, type):
        """Get the lua function to read values from buffers."""
        if type[-2:] in ('8', '16', '32'):
            return type[:-2]
        return type

    def _dict_to_table(self, pydict):
        """Convert a python dictionary to lua table."""
        return '{%s}' % ', '.join('[%i]="%s"' %
                    (i, j) for i, j in pydict.items())


class EnumField(Field):
    def __init__(self, name, type, size, values, strict=True):
        super().__init__(name, type, size)
        self.values = self._dict_to_table(values)
        self.strict = strict

        self.keys = ', '.join(str(i) for i in sorted(values.keys()))
        self.func_type = self._get_func_type(type)

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
            data.append('\tlocal test = %s' % self.values)
            data.append('\tif (test[buffer(%i, %i):%s()] == nil) then' % (
                    offset, self.size, self.func_type))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, "%s")'
                    % (self.name, 'Invalid value, not in (%s)' % self.keys))
            data.append('\tend')

        return '\n'.join(data)


class ArrayField(Field):
    pass


class DissectorField(Field):
    def __init__(self, name, size=None):
        super().__init__(name, 'trailer', size)

    def get_definition(self):
        pass

    def get_code(self, offset):
        if self.size is not None:
            offset = '%s, %s' % (offset, self.size)
        t = '\tlocal subdissector = Dissector.get("{name}")\n' \
            '\tdissector:call(buffer({offset}):tvb(), pinfo, tree)'
        return t.format(offset=offset, name=self.name)


class BitField(Field):
    def __init__(self, name, type, size, values):
        super().__init__(name, type, size)
        self._values = values
        #'local bit = require("bit")'


class RangeField(Field):
    def __init__(self, name, type, size, min, max):
        super().__init__(name, type, size)
        self.min = min
        self.max = max
        self.func_type = self._get_func_type(type)

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

    def __init__(self, name, coord, conf=None):
        self.name = name
        self.coord = coord
        self.conf = conf

        if self.conf and self.conf.id is not None:
            self.id = self.conf.id
        else:
            Protocol.counter += 1
            self.id = Protocol.counter

        if self.conf and self.conf.description is not None:
            self.description = self.conf.description
        else:
            self.description = 'struct %s' % self.name

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
        for field in self.fields:
            code = field.get_definition()
            if code is not None:
                self.data.append(code)
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
            code = field.get_code(offset)
            if code is not None:
                self.data.append(code)
            if field.size is not None:
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

