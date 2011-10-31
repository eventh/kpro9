"""
A module for generating Lua dissectors for Wireshark.

Contains classes for creating dissectors for a specific protocol, which
holds a list of fields which are instances of Field or its subclasses.

Also contains the class which generates a dissector for delegating
dissecting of messages to the specific protocol dissectors.
"""
import string

from platform import Platform


# Reserved keywords in Lua, to avoid using them as variable names
LUA_KEYWORDS = [
    'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
    'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
    'return', 'then', 'true', 'until', 'while'
]


def create_lua_var(var, length=None):
    """Return a valid lua variable name."""
    valid = string.ascii_letters + string.digits + '_'
    if length is None:
        length = len(var)
    var.replace(' ', '_')

    i = 0
    while i < len(var) and i < length:
        if var[i] not in valid:
            var = var[:i] + var[i+1:]
        elif i == 0 and var[i] in string.digits:
            var = var[:i] + var[i+1:]
        else:
            i += 1

    if var in LUA_KEYWORDS:
        var = '_%s' % var

    return var.lower()


def create_lua_valuestring(dict_, wrap=True):
    """Convert a python dictionary to lua table."""
    items = dict_.items()
    if wrap:
        items = [(i, '"%s"' % j) for i, j in items]
    return '{%s}' % ', '.join('[%i]=%s' % (i, j) for i, j in items)


class Field:
    """Represents Wireshark's ProtoFields which stores a specific value."""

    def __init__(self, proto, name, type, size, alignment_size):
        """Create a new Field instance.

        'proto' is the protocol which owns the field
        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        """
        self.proto = proto
        self.name = name
        self.type = type
        self.size = size
        self.alignment_size = alignment_size

        self.add_var = self.proto._get_tree_add() # For adding fields to tree
        self.var = '%s.%s' % (self.proto.field_var, create_lua_var(self.name))
        self.abbr = '%s.%s' % (self.proto.name, self.name.replace(' ', '_'))

        self.base = None # One of 'base.DEC', 'base.HEX' or 'base.OCT'
        self.values = None # Dict with the text that corresponds to the values
        self.mask = None # Integer mask of this field
        self.desc = None # Description of the field
        self.offset = None # Useful for others to access buffer(offset, size)

    def get_definition(self, sequence=None):
        """Get the ProtoField definition for this field."""
        var = self.var
        if sequence is not None:
            var = '%s_%s' % (var, '_'.join([str(i) for i in sequence]))
        return self._create_field(var, self.type, self.abbr,
                self.name, self.base, self.values, self.mask, self.desc)

    def get_code(self, offset, store=None, sequence=None, tree='subtree'):
        """Get the code for dissecting this field."""
        var = self.var
        if sequence is not None:
            var = '%s_%s' % (var, '_'.join([str(i) for i in sequence]))
        if store:
            store = 'local {var} = '.format(var=create_lua_var(store))
        else:
            store = ''
        self.offset = offset

        t = '\t{store}{tree}:{add}({var}, buffer({offset}, {size}))'
        return t.format(store=store, tree=tree, add=self.add_var,
                        var=var, offset=offset, size=self.size)

    def get_padded_offset(self, offset):
        padding = 0
        if(self.alignment_size != 0):
            padding = self.alignment_size - offset % self.alignment_size
            if padding >= self.alignment_size:
                padding = 0
        return offset + padding

    def _create_field(self, var, type_, abbr, name,
            base=None, values=None, mask=None, desc=None):
        """Create a ProtoField definition."""
        template = '{var} = ProtoField.{type}("{abbr}", "{name}"{rest})'
        args = {'var': var, 'type': type_, 'abbr': abbr, 'name': name}

        # Add other parameters if applicable
        if desc is not None:
            desc = '"%s"' % desc

        other = []
        for var in reversed([base, values, mask, desc]):
            if other or var is not None:
                if var is None:
                    var = 'nil'
                other.append(var)

        if other:
            other.append('')
            args['rest'] = ', '.join(reversed(other))
        else:
            args['rest'] = ''

        return template.format(**args)

    def _create_value_var(self, var, offset=None):
        """Create code which stores the field value in 'var'.

        If 'offset' is not provided, must be run after get_code().
        """
        if offset is None:
            offset = self.offset
        store = 'local {var} = buffer({offset}, {size}):{type}()'
        return store.format(var=create_lua_var(var), offset=offset,
                            size=self.size, type=self._get_func_type())

    def _get_func_type(self):
        """Get the lua function to read values from buffers."""
        func_type = self.type
        if func_type[-1] == '8':
            func_type = func_type[:-1]
        if func_type[-2:] in ('16', '32'):
            func_type = func_type[:-2]

        # Endian handling
        if func_type not in ('bytes', 'string', 'stringz', 'ether'):
            if self.proto.platform is not None:
                if self.proto.platform.endian == Platform.little:
                    func_type = 'le_%s' % func_type

        return func_type


class EnumField(Field):
    """A field representing an enum."""

    def __init__(self, proto, name, type, size, alignment_size, values, strict=True):
        """Create a new EnumField.

        'proto' the Protocol which owns the field
        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        'values' is a dict mapping field values to names
        'strict' adds validation of the fields value
        """
        super().__init__(proto, name, type, size, alignment_size)
        self.values = create_lua_valuestring(values)
        self.strict = strict

        self.keys = ', '.join(str(i) for i in sorted(values.keys()))
        self.func_type = self._get_func_type()
        if self.strict:
            self.values_var = create_lua_var('%s_values' % self.name)
        else:
            self.values_var = None
        self.tree_var = create_lua_var(self.name)

    def get_definition(self, sequence = None):
        """Get the ProtoField definition for this field."""
        variable_name = self.var
        if sequence != None:
            postfix = '';
            for index in sequence:
                postfix = '%s_%i' % (postfix, index)
            variable_name = "%s%s" % (self.var, postfix)
        data = []
        if self.strict and (sequence == None or sequence[len(sequence) - 1] == 0):
            data.append('local {var} = {values}'.format(
                    var=self.values_var, values=self.values))
        data.append(self._create_field(variable_name, self.type, self.abbr,
                self.name, self.base, self.values_var, self.mask, self.desc))
        return '\n'.join(data)

    def get_code(self, offset, store=None, sequence=None, tree='subtree'):
        """Get the code for dissecting this field."""
        data = []
        postfix = ''
        if sequence != None:
            for index in sequence:
                postfix = '%s_%i' % (postfix, index)

        # Local var definitions
        if store is not None:
            self.tree_var = store
        if self.strict:
            store = self.tree_var + postfix
        data.append(super().get_code(offset, store, sequence, tree))

        # Add a test which validates the enum value
        if self.strict:
            data.append('\tif (%s[buffer(%i, %i):%s()] == nil) then' % (
                    self.values_var, offset, self.size, self.func_type))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, "%s")'
                    % (create_lua_var(self.tree_var + postfix), 'Invalid value, not in (%s)' % self.keys))
            data.append('\tend')

        return '\n'.join(data)


class ArrayField(Field):
    def __init__(self, proto, name, type, base_size, alignment_size, depth, enum_members=None):
        self.base_size = base_size
        self.depth = depth
        array_size = 1
        for size in self.depth:
            array_size *= size

        self.elements = depth.pop()
        if not depth:
            self.field = self._make_field(proto, name, type, base_size, alignment_size, enum_members)
        else:
            self.field = ArrayField(proto, name, type, base_size, alignment_size, depth)

        super().__init__(proto, name, type, array_size * base_size, alignment_size)

    def _make_field(self, proto, name, type, size, alignment_size, enum_members):
        if isinstance(type, Protocol) or isinstance(type, UnionProtocol):
            return ProtocolField(proto, name, type)

        ctype = proto.platform.map_type(type)
        if enum_members != None:
            return EnumField(proto, name, ctype, size, alignment_size, enum_members)

        if proto.conf:
            bits, enums, ranges, customs = proto.conf.get_field_attributes(name, type)

            ctype = proto.platform.map_type(type)

            # Custom field rules
            if customs:
                custom = customs[0]
                if(custom.size != size or custom.alignment_size != alignment_size):
                    raise "Error: todo"
                field = Field(proto, name, custom.field, size, alignment_size)
                field.abbr = custom.abbr
                field.base = custom.base
                if custom.values:
                    field.values = create_lua_valuestring(custom.values)
                    field.mask = custom.mask
                    field.desc = custom.desc
                    return field

                # Bitstring rules
                if bits:
                    return BitField(proto, name, ctype, size, alignment_size, bits[0].bits)

                # Enum rules
                if enums:
                    rule = enums[0]
                    return EnumField(proto, name, ctype, size, alignment_size, rule.values, rule.strict)
                # Range
                if ranges:
                    rule = ranges[0]
                    return RangeField(proto, name, ctype, size, alignment_size, rule.min, rule.max)

        return Field(proto, name, ctype, size, alignment_size)

    def get_definition(self, sequence=None):
        if sequence is None:
            sequence = []

        data = ['']
        if not sequence:
            data = ['-- Array definition for %s' % self.name]

        type_ = self.type
        if type_ not in ('string', 'stringz'):
            type_ = 'bytes'

        var = self.var
        if sequence:
            var = '%s_%s' % (var, '_'.join(str(i) for i in sequence))

        # This subtree definition
        data.append(self._create_field(var, type_, self.abbr, self.name))

        for i in range(0, self.elements):
            definition = self.field.get_definition(sequence + [i])
            if definition:
                data.append(definition)

        return '\n'.join(data)

    def get_code(self, offset, tree='arraytree', parent='subtree', name='', sequence=[]):
        data = []
        if sequence == []:
            data = ['\t-- Array handling for %s' % self.name]

        postfix = '';
        for index in sequence:
            postfix = '%s_%i' % (postfix, index)

        t = '\tlocal {tree} = {parent}:{add}({var}{postfix}, buffer({off}, {size}))'
        data.append(t.format(tree=tree, parent=parent, add=self.add_var,
                             var=self.var, postfix = postfix, off=offset, size=self.size))

        t = '\t{tree}:set_text("{type} array: index{index})")'
        data.append(t.format(tree=tree, type=self.type, index = postfix))
        for i in range(0, self.elements):
            if  isinstance(self.field, ArrayField):
                data.append(self.field.get_code(offset, 'sub' + tree, tree, name, sequence + [i]))
                offset += self.field.size
            else:
                data.append(self.field.get_code(offset, None, sequence + [i], tree))
                offset += self.field.size

        data.append('')
        return '\n'.join(data)


class ProtocolField(Field):
    def __init__(self, proto, name, sub_proto):
        super().__init__(proto, name, sub_proto.name, sub_proto.get_size(), sub_proto.get_alignment_size())
        self.proto_name = sub_proto.longname

    def get_definition(self, sequence=None):
        pass

    def get_code(self, offset, store=None, sequence=None, tree='subtree'):
        var = self.var
        if sequence is not None:
            var = '%s_%s' % (var, '_'.join([str(i) for i in sequence]))

        t = '\tpinfo.private.caller_def_name = "{name}"\n'\
            '\tDissector.get("{proto}"):call('\
            'buffer({offset},{size}):tvb(), pinfo, {tree})'
        return t.format(name=var, proto=self.proto_name, tree=tree,
                dt=self.proto.DISSECTOR_TABLE, offset=offset, size=self.size)


class BitField(Field):
    def __init__(self, proto, name, type, size, alignment_size, bits):
        super().__init__(proto, name, type, size, alignment_size)
        self.bits = bits

    def _bit_var(self, name):
        return '%s_%s' % (self.var, create_lua_var(name))

    def _bit_abbr(self, name):
        return '%s.%s' % (self.abbr, name.replace(' ', '_'))

    def get_definition(self, sequence=None):
        data = ['-- Bitstring definitions for %s' % self.name]

        postfix = ''
        if sequence != None:
            postfix = '_%s' % '_'.join([str(i) for i in sequence])

        # Bitstrings need to be unsigned for HEX?? Research needed!
        if 'int' in self.type and not self.type.startswith('u'):
            type_ = 'u%s' % self.type
        else:
            type_ = self.type

        # Create bitstring tree definition
        data.append(self._create_field(self.var + postfix, type_,
                self.abbr, '%s (bitstring)' % self.name, base='base.HEX'))

        # Create definitions for all bits
        for i, j, name, values in self.bits:

            # Create a mask for the bits
            tmp = [0] * self.size * 8
            for k in range(j):
                tmp[-(i+k)] = 1
            mask = '0x%x' % int(''.join(str(i) for i in tmp), 2)

            values = create_lua_valuestring(values)
            data.append(self._create_field(self._bit_var(name) + postfix, type_,
                    self._bit_abbr(name), name, values=values, mask=mask))

        return '\n'.join(data)

    def get_code(self, offset, store=None, sequence=None, tree='subtree'):
        data = ['\t-- Bitstring handling for %s' % self.name]

        postfix = ''
        if sequence != None:
            postfix = '_%s' % '_'.join([str(i) for i in sequence])

        buff = 'buffer({off}, {size})'.format(off=offset, size=self.size)
        t = '\tlocal bittree = {tree}:{add}({var}, {buff})'
        data.append(t.format(tree = tree, add=self.add_var, var=self.var + postfix, buff=buff))

        for i, j, name, values in self.bits:
            data.append('\tbittree:{add}({var}, {buff})'.format(
                        add=self.add_var, var=self._bit_var(name) + postfix, buff=buff))

        data.append('')
        return '\n'.join(data)


class RangeField(Field):
    def __init__(self, proto, name, type, size, alignment_size, min, max):
        super().__init__(proto, name, type, size, alignment_size)
        self.min = min
        self.max = max
        self.func_type = self._get_func_type()

    def get_code(self, offset, sequence=None, tree='subtree'):
        """Get the code for dissecting this field."""
        data = []

        postfix = ''
        if sequence != None:
            for index in sequence:
                postfix = '%s_%i' % (postfix, index)

        # Local var definitions
        t = '\tlocal {name} = {tree}:{add}({var}, buffer({off}, {size}))'
        data.append(t.format(var=self.var + postfix, name=create_lua_var(self.name),
                             tree=tree, add=self.add_var, off=offset, size=self.size))

        # Test the value
        def create_test(value, test, warn):
            data.append('\tif (buffer(%i, %i):%s() %s %s) then' %
                    (offset, self.size, self.func_type, test, value))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, '
                            '"Should be %s %s")' % (create_lua_var(self.name), warn, value))
            data.append('\tend')

        if self.min is not None:
            create_test(self.min, '<', 'larger than')
        if self.max is not None:
            create_test(self.max, '>', 'smaller than')

        return '\n'.join(data)


class Protocol:
    """A Protocol is a collection of fields and code.

    It's used to generate Wireshark dissectors written in Lua, for
    dissecting a packet into a set of fields with values.
    """
    DISSECTOR_TABLE = 'luastructs'
    REGISTER_FUNC = 'delegator_register_proto'

    def __init__(self, name, conf=None, platform=None):
        """Create a Protocol, for generating a dissector.

        'name' is the name of the Protocol to dissect
        'conf' is the configuration for this Protocol
        'platform' is the platform the dissector should run on
        """
        if platform is None:
            platform = Platform.mappings['default']
        self.platform = platform
        self.name = name
        self.longname = '%s.%s' % (platform.name.lower(), self.name.lower())
        self.conf = conf

        # Dissector ID
        if self.conf and self.conf.id is not None:
            self.id = self.conf.id
        else:
            self.id = None

        # Dissector description
        if self.conf and self.conf.description is not None:
            self.description = self.conf.description
        else:
            self.description = name
        self.description = '%s (%s)' % (self.description, self.platform.name)

        self.fields = [] # List of all fields in this protocol
        self.data = [] # List of generated content

        # Different lua variables
        self.var = create_lua_var('proto_%s' % name)
        self.field_var = 'f'

    def create(self):
        """Returns all the code for dissecting this protocol."""
        # Create dissector content
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()
        self._register_dissector()
        return '\n'.join(self.data)

    def get_size(self):
        """Find the size of the fields in the protocol."""
        size = 0
        for field in self.fields:
            if field.size:
                size = field.get_padded_offset(size)
                size += field.size

        return self.pad_struct_size(size)

    def pad_struct_size(self, original_size):
        alignment_size = self.get_alignment_size()
        padding = 0
        if alignment_size != 0:
            padding = alignment_size - original_size % alignment_size
            if padding >= alignment_size:
                padding = 0
        return original_size + padding

    def get_alignment_size(self):
        """Find the alignment size of the fields in the protocol."""
        return max([0] + [f.alignment_size
                        for f in self.fields if f.alignment_size])

    def add_field(self, *args, **vargs):
        """Create and add a new Field to the protocol."""
        return self._add(Field(self, *args, **vargs))

    def add_array(self, *args, **vargs):
        """Create and add a new ArrayField to the protocol."""
        return self._add(ArrayField(self, *args, **vargs))

    def add_enum(self, *args, **vargs):
        """Create and add a new EnumField to the protocol."""
        return self._add(EnumField(self, *args, **vargs))

    def add_range(self, *args, **vargs):
        """Create and add a new RangeField to the protocol."""
        return self._add(RangeField(self, *args, **vargs))

    def add_bit(self, *args, **vargs):
        """Create and add a new BitField to the protocol."""
        return self._add(BitField(self, *args, **vargs))

    def add_protocol(self, *args, **vargs):
        """Create and add a new ProtocolField to the protocol."""
        return self._add(ProtocolField(self, *args, **vargs))

    def _add(self, field):
        """Add a field to the protocol, returns the field."""
        self.fields.append(field)
        return field

    def _legal_header(self):
        """Add the legal header with license info."""
        pass

    def _header_defintion(self):
        """Add the code for the header of the protocol."""
        comment = '-- Dissector for %s' % self.longname
        if self.description:
            comment = '%s: %s' % (comment, self.description)
        self.data.append(comment)

        proto = 'local {var} = Proto("{name}", "{description}")\n'
        self.data.append(proto.format(var=self.var, name=self.longname,
                                      description=self.description))

    def _fields_definition(self):
        """Add code for defining the ProtoField's in the protocol."""
        self.data.append('-- ProtoField defintions for: %s' % self.name)
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))

        for field in self.fields:
            code = field.get_definition()

            if self.conf and self.conf.cnf: # Conformance file code
                code = self.conf.cnf.match(field.name, code, defintion=True)
            if code is not None:
                self.data.append(code)

        # Conformance file defintion code extra
        if self.conf and self.conf.cnf:
            code = self.conf.cnf.match(None, None, defintion=True)
            if code:
                self.data.append(code)

        self.data.append('')

    def _fields_code(self, union=False):
        """Add the code from each field into dissector function."""
        offset = 0
        for field in self.fields:
            offset = field.get_padded_offset(offset)
            code = field.get_code(offset)

            if self.conf and self.conf.cnf: # Conformance file code
                code = self.conf.cnf.match(field.name, code, defintion=False)
            if code:
                self.data.append(code)
            if not union and field.size is not None:
                offset += field.size

        # Conformance file dissection function code extra
        if self.conf and self.conf.cnf:
            code = self.conf.cnf.match(None, None, defintion=False)
            if code:
                self.data.append(code)

        return offset

    def _dissector_func(self):
        """Add the code for the dissector function for the protocol."""
        self.data.append('-- Dissector function for: %s' % self.name)
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:{add}({var}, buffer())'
        check = '\tif pinfo.private.caller_def_name then\n\t\t'\
            'subtree:set_text(pinfo.private.caller_def_name .. ": " .. {var}.'\
            'description)\n\t\tpinfo.private.caller_def_name = nil\n\telse\n'\
            '\t\tpinfo.cols.info:append(" (" .. {var}.description .. ")")\n'\
            '\tend\n'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(
                add=self._get_tree_add(), var=self.var))
        self.data.append(check.format(var=self.var))

        offset = self._fields_code()

        # Delegate rest of buffer to any trailing protocols
        if self.conf and self.conf.trailers:
            self._trailers(self.conf.trailers, offset)

        self.data.append('end\n')

    def _register_dissector(self):
        """Add code for registering the dissector in the dissector table."""
        if self.id is None:
            id = 'nil'
        else:
            id = self.id
        self.data.append('{func}({var}, "{platform}", "{name}", {id})'.format(
                func=self.REGISTER_FUNC, var=self.var, name=self.name,
                platform=self.platform.name, id=id))
        self.data.append('')

    def _trailers(self, rules, offset):
        """Add code for handling of trailers to the protocol."""
        self.data.append('\n\t-- Trailers handling for struct: %s' % self.name)

        # Offset variable and variable declaration
        off_var = 'trail_offset'
        t_offset = '\tlocal {var} = {offset}'
        self.data.append(t_offset.format(offset=offset, var=off_var))

        for i, rule in enumerate(rules):
            # Find the count
            if rule.member is not None:
                # Find offset, size and func_type
                fields = [i for i in self.fields if i.name == rule.member]
                if not fields:
                    continue # rule.member don't exists in the struct
                func = fields[0]._get_func_type()

                count = 'trail_count'
                t = '\tlocal {var} = buffer({off}, {size}):{func}()'
                self.data.append(t.format(off=fields[0].offset,
                                 var=count, size=fields[0].size, func=func))
            else:
                count = rule.count

            size_str = ''
            if rule.size is not None:
                size_str = ', %i' % rule.size

            # Call trailers 'count' times
            tabs = '\t'
            if rule.member is not None or count > 1:
                self.data.append('\tfor i = 1, {count} do'.format(count=count))
                tabs += '\t'

            t1 = '{tabs}local trailer = Dissector.get("{name}")'
            t2 = '{tabs}trailer:call(buffer({off}{size}):tvb(), pinfo, tree)'
            t3 = '{tabs}{var} = {var} + {size}'
            self.data.append(t1.format(tabs=tabs, name=rule.name))
            self.data.append(t2.format(tabs=tabs, off=off_var, size=size_str))

            # Update offset after all but last trailer
            if i < len(rules)-1:
                self.data.append(t3.format(tabs=tabs,
                                           var=off_var, size=rule.size))

            if rule.member is not None or count > 1:
                self.data.append('\tend') # End for loop

    def _get_tree_add(self):
        """Get the endian specific function for adding a item to a tree."""
        if self.platform and self.platform.endian == Platform.little:
            return 'add_le'
        return 'add'


class UnionProtocol(Protocol):
    def __init__(self, name, conf=None, platform=None):
        super().__init__(name, conf, platform)

    def get_size(self):
        """Find the size of the fields in the protocol."""
        return self.pad_struct_size(max(
                [0] + [field.size for field in self.fields if field.size]))

    def _fields_code(self):
        """Add the code from each field into dissector function."""
        super()._fields_code(union=True)
        return self.get_size()


class Delegator(Protocol):
    """A class for delegating dissecting to protocols.

    Creates the top-level lua dissector which delegates the task
    of dissecting specific messages to dissectors generated by
    Protocol instances.

    This top-level dissector contains code for finding the platform
    the message originates from, and finds which specific dissector
    handles that platform and message.
    """

    def __init__(self, platforms):
        self.platforms = platforms
        name = self.DISSECTOR_TABLE

        super().__init__(name, None, Platform.mappings['default'])

        self.longname = name
        self.description = 'Lua C Structs'
        self.id = None

        self.var = create_lua_var('delegator')
        self.table_var = create_lua_var('dissector_table')
        self.id_table = create_lua_var('message_ids')
        self.msg_var = create_lua_var('msg_node')

        # Add fields, don't change sizes!
        values = {p.flag: p.name for name, p in self.platforms.items()}
        self.add_field('Version', 'uint8', 1, 0)
        self.add_enum('Flags', 'uint8', 1, 0, values)
        self.add_enum('Message', 'uint16', 2, 0, {}, strict=False)
        self.add_field('Message length', 'uint32', 4, 0)
        self._version, self._flags, self._msg_id, self._length = self.fields

    def create(self):
        """Returns all the code for dissecting this protocol."""
        self._header_defintion()
        self._fields_definition()
        self._register_function()
        self._dissector_func()
        self.data.append('\n')
        return '\n'.join(self.data)

    def _header_defintion(self):
        """Add the code for the header of the protocol."""
        self.data.append('-- Delegator for %s dissectors' % self.name)

        # Create the different dissector tables
        t = 'local {var} = DissectorTable.new("{short}", "Lua Structs", ftypes.STRING)'
        self.data.append(t.format(var=self.table_var, short=self.name))

        # Create the delegator dissector
        proto = 'local {var} = Proto("{name}", "{description}")'
        self.data.append(proto.format(var=self.var, name=self.name,
                                      description=self.description))

        # Add the message id table
        self.data.append('local {var} = {{}}\n'.format(var=self.id_table))

    def _register_function(self):
        """Add code for register protocol function."""
        self.data.append('-- Register struct dissectors')
        t = 'function {func}(proto, platform, name, id)\n'\
                '\t{table}:add(platform .. "." .. name, proto)\n'\
                '\tif (id ~= nil) then {ids}[id] = name end\nend\n'
        self.data.append(t.format(func=self.REGISTER_FUNC,
                         table=self.table_var, ids=self.id_table))

    def _dissector_func(self):
        """Add the code for the dissector function for the protocol."""
        # Add dissector function
        self.data.append('-- Delegator dissector function for %s' % self.name)
        self.data.append('function delegator.dissector(buffer, pinfo, tree)')
        self.data.append('\tlocal subtree = tree:add(delegator, buffer())')
        self.data.append('\tpinfo.cols.protocol = delegator.name')
        self.data.append('\tpinfo.cols.info = delegator.description\n')

        # Fields code
        self.data.append(self._version.get_code(0))
        self.data.append(self._flags.get_code(1))
        self.data.append(self._msg_id.get_code(2, store=self.msg_var))

        t = '\tsubtree:add(f.messagelength, buffer(4):len()):set_generated()'
        self.data.extend([t, ''])

        # Find message id and flag
        flags_var = create_lua_var('flags')
        msg_var = create_lua_var('message_id')
        self.data.append('\t' + self._flags._create_value_var(flags_var))
        self.data.append('\t' + self._msg_id._create_value_var(msg_var))

        # Validate message id
        t = '\tif ({ids}[{msg}] == nil) then\n\t\t{node}:add_expert_info'\
            '(PI_MALFORMED, PI_WARN, "Unknown message id")\n\telse\n'\
            '\t\t{node}:append_text(" (" .. {ids}[{msg}] ..")")\n\tend\n'
        self.data.append(t.format(
                ids=self.id_table, msg=msg_var, node=self.msg_var))

        # Call the right dissector
        t = '\tif ({flags}[{flag}] ~= nil and {ids}[{msg}] ~= nil) then'\
            '\n\t\tlocal name = {flags}[{flag}] .. "." .. {ids}[{msg}]'\
            '\n\t\t{table}:try(name, buffer(4):tvb(), pinfo, tree)'\
            '\n\tend\nend'
        self.data.append(t.format(flags=self._flags.values_var, msg=msg_var,
                flag=flags_var, ids=self.id_table, table=self.table_var))

