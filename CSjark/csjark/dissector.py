"""
A module for generating LUA dissectors for Wireshark.
"""
import string

INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
VALID_PROTOFIELD_TYPES = INT_TYPES + OTHER_TYPES


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
    return var


class Field:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

        self.abbr = None
        self.base = None # One of 'base.DEC', 'base.HEX' or 'base.OCT'
        self.values = None # Dict with the text that corresponds to the values
        self.mask = None # Integer mask of this field
        self.desc = None # Description of the field
        self.offset = None # Useful for others to access buffer(offset, size)

    def set_protocol(self, proto):
        self.proto = proto
        self.var = '%s.%s' % (self.proto.field_var, self.name)
        if self.abbr is None:
            self.abbr = '%s.%s' % (self.proto.name, self.name)

    def create_field(self, var, type_, abbr, name,
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

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        return self.create_field(self.var, self.type, self.abbr,
                self.name, self.base, self.values, self.mask, self.desc)

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        self.offset = offset
        t = '\tsubtree:add({var}, buffer({offset}, {size}))'
        return t.format(var=self.var, offset=offset, size=self.size)

    def _get_func_type(self):
        """Get the lua function to read values from buffers."""
        if self.type[-2:] in ('8', '16', '32'):
            return self.type[:-2]
        return self.type

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
        self.func_type = self._get_func_type()

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        t = '\tlocal {name} = subtree:add({var}, buffer({offset}, {size}))'
        data.append(t.format(name=self.name, var=self.var,
                             offset=offset, size=self.size))

        # Add a test which validates the enum value
        if self.strict:
            data.append('\tlocal test = %s' % self.values)
            data.append('\tif (test[buffer(%i, %i):%s()] == nil) then' % (
                    offset, self.size, self.func_type))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, "%s")'
                    % (self.name, 'Invalid value, not in (%s)' % self.keys))
            data.append('\tend')

        return '\n'.join(data)


class ArrayField(Field):
    def __init__(self, name, type, base_size, depth):
        self.base_size = base_size
        self.depth = depth
        self.elements = 1 # Number of total elements in the array
        for size in self.depth:
            self.elements *= size

        super().__init__(name, type, self.elements * self.base_size)
        self.func_type = self._get_func_type()

    def get_definition(self):
        data = ['-- Array definition for %s' % self.name]

        # Create fields for subtrees in the array
        i = 0
        type_ = self.type
        if type_ not in ('string', 'stringz'):
            type_ = 'bytes'
        for k, size in enumerate(self.depth):
            if len(self.depth) > 1 and k == len(self.depth) - 1:
                continue # Multi-dim array, no subtree last depth level
            for j in range(size):
                data.append(self.create_field('%s_%i' % (self.var, i),
                        type_, self.abbr, self.name))
                i += 1

        # Create fields for each element in the array
        for i in range(self.elements):
            data.append(self.create_field('%s__%i' % (self.var, i),
                    self.type, '%s.%i' % (self.abbr, i), '[%i]' % i))

        return '\n'.join(data)

    def get_code(self, offset):
        data = ['\t-- Array handling for %s' % self.name]
        element = 0 # Count of which array element we have created
        subtree = 0 # Count of which subtree we have created

        def subdefinition(tree, parent, elem, name=''):
            """Create a subtree of arrays."""
            nonlocal element, offset, subtree

            # Create the subtree
            size = elem * self.base_size
            t = '\tlocal {tree} = {old}:add({var}_{i}, buffer({off}, {size}))'
            data.append(t.format(tree=tree,
                    old=parent, var=self.var, i=subtree, off=offset, size=size))

            # Set a more usefull text to the subtree
            if name:
                name += ' '
            t = '\t{tree}:set_text("{name}(array: {size} x {type})")'
            data.append(t.format(tree=tree,
                    name=name, size=elem, type=self.type))

            subtree += 1

        def addfield(tree):
            """Add value from buffer to the elements field."""
            nonlocal element, offset
            t = '\t{tree}:add({var}__{i}, buffer({offset}, {size}))'
            data.append(t.format(tree=tree, offset=offset,
                    size=self.base_size, var=self.var, i=element))
            element += 1
            offset += self.base_size

        def array(depth, tree, parent):
            """Recursively add elements to array tree."""
            if len(depth) == 1:
                for i in range(depth[0]):
                    addfield(tree)
            else:
                size = depth.pop(0)
                elements = 1
                for k in depth:
                    elements *= k
                parent = tree
                tree = 'sub%s' % tree
                for i in range(size):
                    subdefinition(tree, parent, elements)
                    array(depth, tree, parent)

        parent = 'subtree'
        tree = 'arraytree'
        subdefinition(tree, parent, self.elements, self.name)
        array(self.depth[:], tree, parent)

        data.append('')
        return '\n'.join(data)


class ProtocolField(Field):
    def __init__(self, name, id, size, type_name):
        super().__init__(name, type_name, size)
        self.id = id

    def get_definition(self):
        pass

    def get_code(self, offset):
        t = '\tlocal subsubtree = subtree:add("{name}:")\n' \
            '\tluastructs_dt:try({id}, buffer({offset},' \
            '{size}):tvb(), pinfo, subsubtree)'
        return t.format(name=self.name, id=self.id,
                        offset=offset, size=self.size)


class BitField(Field):
    def __init__(self, name, type, size, bits):
        super().__init__(name, type, size)
        self.bits = bits

    def _bit_var(self, name):
        return '%s_%s' % (self.var, create_lua_var(name))

    def _bit_abbr(self, name):
        return '%s.%s' % (self.abbr, name.replace(' ', '_'))

    def get_definition(self):
        data = ['-- Bitstring definitions for %s' % self.name]

        # Bitstrings need to be unsigned for HEX?? Research needed!
        if 'int' in self.type and not self.type.startswith('u'):
            type_ = 'u%s' % self.type
        else:
            type_ = self.type

        # Create bitstring tree definition
        data.append(self.create_field(self.var, type_,
                self.abbr, '%s (bitstring)' % self.name, base='base.HEX'))

        # Create definitions for all bits
        for i, j, name, values in self.bits:

            # Create a mask for the bits
            tmp = [0] * self.size * 8
            for k in range(j):
                tmp[-(i+k)] = 1
            mask = '0x%x' % int(''.join(str(i) for i in tmp), 2)

            values = self._dict_to_table(values)
            data.append(self.create_field(self._bit_var(name), type_,
                    self._bit_abbr(name), name, values=values, mask=mask))

        return '\n'.join(data)

    def get_code(self, offset):
        data = ['\t-- Bitstring handling for %s' % self.name]

        buff = 'buffer({off}, {size})'.format(off=offset, size=self.size)
        t = '\tlocal bittree = subtree:add({var}, {buff})'
        data.append(t.format(var=self.var, buff=buff))

        for i, j, name, values in self.bits:
            data.append('\tbittree:add({var}, {buff})'.format(
                                var=self._bit_var(name), buff=buff))

        data.append('')
        return '\n'.join(data)


class RangeField(Field):
    def __init__(self, name, type, size, min, max):
        super().__init__(name, type, size)
        self.min = min
        self.max = max
        self.func_type = self._get_func_type()

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        t = '\tlocal {name} = subtree:add({var}, buffer({off}, {size}))'
        data.append(t.format(var=self.var, name=self.name,
                             off=offset, size=self.size))

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


class CustomField(Field):
    """A Field defined by a Custom rule."""

    def __init__(self, name, type, size, rule):
        super().__init__(name, type, size)
        self.rule = rule

    def get_definition(self):
        return super().get_definition()

    def get_code(self, offset):
        return super().get_code(offset)


class Protocol:
    """A Protocol is a collection of fields and code.

    It's used to generate Wireshark dissectors written in Lua, for
    dissecting a packet into a set of fields with values.
    """
    counter = 0 # Used to give protocols unique IDs if needed

    def __init__(self, name, coord=None, conf=None):
        """Create a Protocol, for generating a dissector.

        'name' is the name of the Protocol to dissect.
        'coord' is the source location (file and line).
        'conf' is the configuration for this Protocol.
        """
        self.name = name
        self.coord = coord
        self.conf = conf

        # Dissector ID
        if self.conf and self.conf.id is not None:
            self.id = self.conf.id
        else:
            Protocol.counter += 1
            self.id = Protocol.counter

        # Dissector description
        if self.conf and self.conf.description is not None:
            self.description = self.conf.description
        else:
            self.description = 'struct %s' % self.name

        self.fields = []
        self.data = []
        self.var = 'proto_{name}'.format(name=self.name)
        self.field_var = 'f'
        self.dissector = 'luastructs.message'
        self.dissector_table = 'luastructs_dt'

    def get_size(self):
        """Find the size of the fields in the protocol."""
        return sum(field.size for field in self.fields if field)

    def _add(self, field):
        """Add a field to the protocol, updates the fields proto reference."""
        field.set_protocol(self)
        self.fields.append(field)
        return field

    def add_field(self, *args, **vargs):
        """Create and add a new Field to the protocol."""
        return self._add(Field(*args, **vargs))

    def add_array(self, *args, **vargs):
        """Create and add a new ArrayField to the protocol."""
        return self._add(ArrayField(*args, **vargs))

    def add_enum(self, *args, **vargs):
        """Create and add a new EnumField to the protocol."""
        return self._add(EnumField(*args, **vargs))

    def add_range(self, *args, **vargs):
        """Create and add a new RangeField to the protocol."""
        return self._add(RangeField(*args, **vargs))

    def add_bit(self, *args, **vargs):
        """Create and add a new BitField to the protocol."""
        return self._add(BitField(*args, **vargs))

    def add_custom(self, *args, **vargs):
        """Create and add a new CustomField to the protocol."""
        return self._add(CustomField(*args, **vargs))

    def add_protocol(self, *args, **vargs):
        """Create and add a new ProtocolField to the protocol."""
        return self._add(ProtocolField(*args, **vargs))

    def _legal_header(self):
        """Add the legal header with license info."""
        pass

    def _header_defintion(self):
        """Add the code for the header of the protocol."""
        comment = '-- Dissector for struct: %s' % self.name
        if self.description:
            comment = '%s: %s' % (comment, self.description)
        self.data.append(comment)

        proto = 'local {var} = Proto("{name}", "{description}")'
        self.data.append(proto.format(var=self.var, name=self.name,
                                      description=self.description))

        table = 'local {table} = DissectorTable.get("{dissector}")'
        self.data.append(table.format(dissector=self.dissector,
                                      table=self.dissector_table))
        self.data.append('')

    def _fields_definition(self):
        """Add code for defining the ProtoField's in the protocol."""
        self.data.append('-- ProtoField defintions for struct: %s' % self.name)
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))
        for field in self.fields:
            code = field.get_definition()
            if code is not None:
                self.data.append(code)
        self.data.append('')

    def _dissector_func(self):
        """Add the code for the dissector function for the protocol."""
        self.data.append('-- Dissector function for struct: %s' % self.name)
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

        # Delegate rest of buffer to any trailing protocols
        if self.conf and self.conf.trailers:
            self._trailers(self.conf.trailers, offset)

        self.data.append('end')
        self.data.append('')

    def _trailers(self, rules, offset):
        """Add code for handling of trailers to the protocol."""
        self.data.append('\n\t-- Trailers handling for struct: %s' % self.name)

        # Offset variable and variable declaration
        offset_var = 'trail_offset'
        t_offset = '\tlocal {var} = {offset}'
        self.data.append(t_offset.format(offset=offset, var=offset_var))

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
            t1 = '\tlocal trailer = Dissector.get("{name}")'
            t2 = '\ttrailer:call(buffer({off}{size}):tvb(), pinfo, tree)'

            # Add for loop if neceseary
            if rule.member is not None or count > 1:
                self.data.append('\tfor i = 1, {count} do'.format(count=count))
                t1 = '\t%s' % t1
                t2 = '\t%s' % t2
                t3 = '\t\t{var} += i * {size}'
            else:
                t3 = '\t{var} += {size}'

            self.data.append(t1.format(name=rule.name))
            self.data.append(t2.format(off=offset_var, size=size_str))

            # Update offset after all but last trailer
            if i < len(rules)-1:
                self.data.append(t3.format(var=offset_var, size=rule.size))

            if rule.member is not None or count > 1:
                self.data.append('\tend') # End for loop

    def _cnf_rules(self, rule):
        """Handle custom lua file for this protocol."""
        return ''
        text = '-- Custom lua file %s for struct %s' % (rule.file, self.name)
        text = '%s\n%s' % (text, rule.contents)

        # Interpolate dissector func
        if '{DEFAULT_BODY}' in text:
            self.data = []
            self._dissector_func()
            text = text.format(DEFAULT_BODY='\n'.join(self.data))

        return text

    def create(self):
        """Returns all the code for dissecting this protocol."""
        # Handle custom lua file rules
        if self.conf and self.conf.cnf is not None:
            return self._cnf_rules(self.conf.cnf)

        # Create dissector content
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()

        # Add code for registering the protocol
        end = 'luastructs_dt:add({id}, {var})\n'
        self.data.append(end.format(id=self.id, var=self.var))

        return '\n'.join(self.data)

