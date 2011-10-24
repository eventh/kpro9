"""
A module for generating Lua dissectors for Wireshark.

Contains classes for creating dissectors for a specific protocol, which
holds a list of fields which are instances of Field or its subclasses.

Also contains the class which generates a dissector for delegating
dissecting of messages to the specific protocol dissectors.
"""
import string

from platform import Platform


# Not used yet, maybe remove it?
#INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
#OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
#                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]
#VALID_PROTOFIELD_TYPES = INT_TYPES + OTHER_TYPES

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
    if not dict_:
        return 'nil'

    items = dict_.items()
    if wrap:
        items = [(i, '"%s"' % j) for i, j in items]

    return '{%s}' % ', '.join('[%i]=%s' % (i, j) for i, j in items)


class Field:
    """Represents Wireshark's ProtoFields which stores a specific value."""

    def __init__(self, proto, name, type, size):
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

        self.add_var = self.proto._get_tree_add() # For adding fields to tree
        self.var = '%s.%s' % (self.proto.field_var, create_lua_var(self.name))
        self.abbr = '%s.%s' % (self.proto.name, self.name.replace(' ', '_'))

        self.base = None # One of 'base.DEC', 'base.HEX' or 'base.OCT'
        self.values = None # Dict with the text that corresponds to the values
        self.mask = None # Integer mask of this field
        self.desc = None # Description of the field
        self.offset = None # Useful for others to access buffer(offset, size)

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        return self._create_field(self.var, self.type, self.abbr,
                self.name, self.base, self.values, self.mask, self.desc)

    def get_code(self, offset, store=''):
        """Get the code for dissecting this field."""
        if store:
            store = 'local {var} = '.format(var=create_lua_var(store))
        self.offset = offset
        t = '\t{store}subtree:{add}({var}, buffer({offset}, {size}))'
        return t.format(store=store, add=self.add_var,
                        var=self.var, offset=offset, size=self.size)

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

    def __init__(self, proto, name, type, size, values, strict=True):
        """Create a new EnumField.

        'proto' the Protocol which owns the field
        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        'values' is a dict mapping field values to names
        'strict' adds validation of the fields value
        """
        super().__init__(proto, name, type, size)
        self.values = create_lua_valuestring(values)
        self.strict = strict

        self.keys = ', '.join(str(i) for i in sorted(values.keys()))
        self.func_type = self._get_func_type()
        self.values_var = create_lua_var('%s_values' % self.name)
        self.tree_var = create_lua_var(self.name)

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        data = []
        data.append('local {var} = {values}'.format(
                var=self.values_var, values=self.values))
        data.append(self._create_field(self.var, self.type, self.abbr,
                self.name, self.base, self.values_var, self.mask, self.desc))
        return '\n'.join(data)

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        data.append(super().get_code(offset, store=self.tree_var))

        # Add a test which validates the enum value
        if self.strict:
            data.append('\tif (%s[buffer(%i, %i):%s()] == nil) then' % (
                    self.values_var, offset, self.size, self.func_type))
            data.append('\t\t%s:add_expert_info(PI_MALFORMED, PI_WARN, "%s")'
                    % (self.tree_var, 'Invalid value, not in (%s)' % self.keys))
            data.append('\tend')

        return '\n'.join(data)


class ArrayField(Field):
    def __init__(self, proto, name, type, base_size, depth):
        self.base_size = base_size
        self.depth = depth
        self.elements = 1 # Number of total elements in the array
        for size in self.depth:
            self.elements *= size

        super().__init__(proto, name, type, self.elements * self.base_size)
        self.func_type = self._get_func_type()

    def get_definition(self):
        data = ['-- Array definition for %s' % self.name]

        # Create fields for subtrees in the array
        i = 0
        type_ = self.type
        if type_ not in ('string', 'stringz'):
            type_ = 'bytes'

        # Top-level subtree
        data.append(self._create_field('%s_%i' % (
                    self.var, i), type_, self.abbr, self.name))
        i += 1

        for k, size in enumerate(self.depth):
            if len(self.depth) > 1 and k == len(self.depth) - 1:
                continue # Multi-dim array, no subtree last depth level
            for j in range(size):
                data.append(self._create_field('%s_%i' % (self.var, i),
                        type_, self.abbr, self.name))
                i += 1

        # Create fields for each element in the array
        for i in range(self.elements):
            data.append(self._create_field('%s__%i' % (self.var, i),
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
            t = '\tlocal {tree} = {old}:{add}({var}_{i}, buffer({off}, {size}))'
            data.append(t.format(tree=tree, old=parent, add=self.add_var,
                        var=self.var, i=subtree, off=offset, size=size))

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
            t = '\t{tree}:{add}({var}__{i}, buffer({offset}, {size}))'
            data.append(t.format(tree=tree, offset=offset, add=self.add_var,
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
    def __init__(self, proto, name, id, size, type_name):
        super().__init__(proto, name, type_name, size)
        self.id = id

    def get_definition(self):
        pass

    def get_code(self, offset):
        t = '\tpinfo.private.struct_def_name = "{name}"\n' \
            '\tluastructs_dt:try({id}, buffer({offset},' \
            '{size}):tvb(), pinfo, subtree)'
        return t.format(name=self.name, id=self.id,
                        offset=offset, size=self.size)


class BitField(Field):
    def __init__(self, proto, name, type, size, bits):
        super().__init__(proto, name, type, size)
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
        data.append(self._create_field(self.var, type_,
                self.abbr, '%s (bitstring)' % self.name, base='base.HEX'))

        # Create definitions for all bits
        for i, j, name, values in self.bits:

            # Create a mask for the bits
            tmp = [0] * self.size * 8
            for k in range(j):
                tmp[-(i+k)] = 1
            mask = '0x%x' % int(''.join(str(i) for i in tmp), 2)

            values = create_lua_valuestring(values)
            data.append(self._create_field(self._bit_var(name), type_,
                    self._bit_abbr(name), name, values=values, mask=mask))

        return '\n'.join(data)

    def get_code(self, offset):
        data = ['\t-- Bitstring handling for %s' % self.name]

        buff = 'buffer({off}, {size})'.format(off=offset, size=self.size)
        t = '\tlocal bittree = subtree:{add}({var}, {buff})'
        data.append(t.format(add=self.add_var, var=self.var, buff=buff))

        for i, j, name, values in self.bits:
            data.append('\tbittree:{add}({var}, {buff})'.format(
                        add=self.add_var, var=self._bit_var(name), buff=buff))

        data.append('')
        return '\n'.join(data)


class RangeField(Field):
    def __init__(self, proto, name, type, size, min, max):
        super().__init__(proto, name, type, size)
        self.min = min
        self.max = max
        self.func_type = self._get_func_type()

    def get_code(self, offset):
        """Get the code for dissecting this field."""
        data = []

        # Local var definitions
        t = '\tlocal {name} = subtree:{add}({var}, buffer({off}, {size}))'
        data.append(t.format(var=self.var, name=create_lua_var(self.name),
                             add=self.add_var, off=offset, size=self.size))

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
    """A Protocol is a collection of fields and code.

    It's used to generate Wireshark dissectors written in Lua, for
    dissecting a packet into a set of fields with values.
    """

    def __init__(self, name, conf=None, platform=None):
        """Create a Protocol, for generating a dissector.

        'name' is the name of the Protocol to dissect
        'conf' is the configuration for this Protocol
        'platform' is the platform the dissector should run on
        """
        self.name = name
        self.conf = conf
        self.platform = platform

        # Dissector ID
        self.id = None
        if self.conf and self.conf.id is not None:
            self.id = self.conf.id

        # Dissector description
        if self.conf and self.conf.description is not None:
            self.description = self.conf.description
        else:
            self.description = 'struct %s' % self.name

        self.fields = []
        self.data = []
        self.var = create_lua_var('proto_%s' % self.name)
        self.field_var = 'f'
        self.table_var = create_lua_var('dissector_table')

    def create(self):
        """Returns all the code for dissecting this protocol."""
        # Create dissector content
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()

        # Add code for registering the protocol
        end = '{table}:add("{name}", {var})\n\n'
        self.data.append(end.format(table=self.table_var,
                         name=self.name, var=self.var))

        return '\n'.join(self.data)

    def get_size(self):
        """Find the size of the fields in the protocol."""
        return sum(field.size for field in self.fields if field)

    def _add(self, field):
        """Add a field to the protocol, returns the field."""
        self.fields.append(field)
        return field

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

        self.data.append('local {var} = DissectorTable.get("{dt}")\n'.format(
                         dt=self.platform.dt_name, var=self.table_var))

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

    def _fields_code(self):
        """Add the code from each field into dissector function."""
        offset = 0
        for field in self.fields:
            code = field.get_code(offset)
            if self.conf and self.conf.cnf:
                code = self._cnf_field_code(field, code)
            if code:
                self.data.append(code)
            if field.size is not None:
                offset += field.size
        return offset

    def _dissector_func(self):
        """Add the code for the dissector function for the protocol."""
        self.data.append('-- Dissector function for struct: %s' % self.name)
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:{add}({var}, buffer())'
        name_check = '\tif pinfo.private.struct_def_name then\n\t\t'\
            'subtree:set_text(pinfo.private.struct_def_name .. ": " .. {var}.'\
            'description)\n\t\tpinfo.private.struct_def_name = nil\n\tend\n'
        desc = '\tpinfo.cols.info:append(" (" .. {var}.description .. ")")'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(
                add=self._get_tree_add(), var=self.var))
        self.data.append(name_check.format(var=self.var))
        self.data.append(desc.format(var=self.var))
        self.data.append('')

        offset = self._fields_code()

        # Delegate rest of buffer to any trailing protocols
        if self.conf and self.conf.trailers:
            self._trailers(self.conf.trailers, offset)

        self.data.append('end\n\n')

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

    def _cnf_field_code(self, field, code):
        """Modify fields code if a cnf file demands it."""
        if field.name in self.conf.cnf.rules:
            rules = self.conf.cnf.rules[field.name]

            # Header rule, insert custom lua before generated code
            if self.conf.cnf.t_hdr in rules:
                return '%s\n%s' % (rules[self.conf.cnf.t_hdr], code)

            # Body rules, replace custom lua with generated code
            elif self.conf.cnf.t_body in rules:
                content = rules[self.conf.cnf.t_body]
                if '%(DEFAULT_BODY)s' in content:
                    content = content.replace('%(DEFAULT_BODY)s', code)
                if '{DEFAULT_BODY}' in content:
                    content = content.format(DEFAULT_BODY=code)
                return content

        return code

    def _get_tree_add(self):
        """Get the endian specific function for adding a item to a tree."""
        if self.platform and self.platform.endian == Platform.little:
            return 'add_le'
        return 'add'


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
        super().__init__('luastructs', None, Platform.mappings['default'])

        self.description = 'Lua C Structs'
        self.id = None
        self.var = create_lua_var('delegator')

        # Add fields, don't change sizes!
        values = {p.flag: p.name for name, p in self.platforms.items()}
        self.add_field('Version', 'uint8', 1)
        self.add_enum('Flags', 'uint8', 1, values)
        self.add_enum('Message', 'uint16', 2, {})
        self.add_field('Message length', 'uint32', 4)
        self._version, self._flags, self._msg_id, self._length = self.fields

    def create(self, all_protocols):
        """Returns all the code for dissecting this protocol."""
        # Update Message id valuestring and keys
        messages = {}
        for plat, protocols in all_protocols.items():
            for name, proto in protocols.items():
                if proto.id is not None:
                    messages[proto.id] = name

        self._msg_id.values = create_lua_valuestring(messages)
        self._msg_id.keys = ', '.join(str(i) for i in sorted(messages.keys()))

        # Create dissector content
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()
        self.data.append('\n')
        return '\n'.join(self.data)

    def _header_defintion(self):
        """Add the code for the header of the protocol."""
        self.data.append('-- Delegator for %s dissectors' % self.name)

        # Create the different dissector tables
        for name, p in self.platforms.items():
            p._var = create_lua_var('dt_%s' % name)
            t = 'local {var} = DissectorTable.new("{short}", "{name}", FT_STRING)'
            self.data.append(t.format(var=p._var, short=p.dt_name,
                                      name='Lua Structs (%s)' % p.name))

        # Create the delegator dissector
        proto = 'local {var} = Proto("{name}", "{description}")'
        self.data.append(proto.format(var=self.var, name=self.name,
                                      description=self.description))
        self.data.append('')

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
        self.data.append(self._msg_id.get_code(2))

        # Store buffer values in variables
        flags_var = create_lua_var('flags')
        msg_var = create_lua_var('message_id')
        self.data.append('\t' + self._flags._create_value_var(flags_var))
        self.data.append('\t' + self._msg_id._create_value_var(msg_var))
        self.data.append('')

        # Find message id and call right dissector
        tables = {p.flag: p._var for name, p in self.platforms.items()}
        t1 = '\tsubtree:add(f.messagelength, buffer(4):len()):set_generated()'
        t2 = '\tlocal tables = %s' % create_lua_valuestring(tables, wrap=False)
        t3 = '\ttables[{flag}]:try({values}[{msg}], buffer(4):tvb(), pinfo, tree)'
        self.data.extend([t1, t2])
        self.data.append(t3.format(flag=flags_var,
                values=self._msg_id.values_var, msg=msg_var))
        self.data.append('end')

