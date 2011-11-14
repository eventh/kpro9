"""
A module for generating Lua dissectors for Wireshark.

Contains classes for creating dissectors for a specific protocol, which
holds a list of fields which are instances of Field or its subclasses.

Also contains the class which generates a dissector for delegating
dissecting of messages to the specific protocol dissectors.
"""
from platform import Platform
from field import create_lua_var, BaseField, Field


class Dissector(BaseField):
    """A Dissector is a collection of fields and code.

    It's used to generate Wireshark dissectors written in Lua, for
    dissecting a packet into a set of fields with values.
    """

    def __init__(self, proto, platform):
        self.proto = proto
        self.platform = platform
        self.endian = platform.endian
        self.name = proto.name
        self.field_var = '%s.%s' (proto.field_var, platform.name)
        self.children = [] # List of all child fields

        self._pushed = False
        self._increase_offset = True

    @property
    def alignment(self):
        """Find the alignment size of the fields in the protocol."""
        return max([0] + [f.alignment for f in self.children])

    @property
    def size(self):
        """Find the size of the fields in the protocol."""
        size = 0
        for field in self.children:
            if field.size:
                size = self.get_padding(field, size)
                size += field.size
        return self.get_padding(self, size)

    def push_modifiers(self):
        """Push prefixes and postfixes down to child fields."""
        if self._pushed:
            return
        self._pushed = True
        for field in self.children:
            field.var_prefix.insert(0, self.field_var)
            field.abbr_prefix.insert(0, self.name)
            field.push_modifiers()

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        data = []

        for field in self.children:
            code = field.get_definition()

            if self.conf and self.conf.cnf: # Conformance file code
                code = self.conf.cnf.match(field.name, code, definition=True)
            data.append(code)

        # Conformance file definition code extra
        if self.conf and self.conf.cnf:
            data.append(self.conf.cnf.match(None, None, definition=True))

        return '\n'.join(i for i in data if i is not None)

    def get_code(self, offset, store=None, tree='subtree'):
        """Get the code for dissecting this field."""
        self.offset = offset
        data = []

        for field in self.children:
            offset = self.get_padding(field, offset)
            code = field.get_code(offset, store=store, tree=tree)

            # Conformance file code
            if self.conf and self.conf.cnf:
                code = self.conf.cnf.match(field.name, code, False, field)
            data.append(code)

            if self._increase_offset:
                offset += field.size

        # Conformance file dissection function code extra
        if self.conf and self.conf.cnf:
            data.append(self.conf.cnf.match(None, None, definition=False))

        # Delegate rest of buffer to any trailing protocols
        if self.conf and self.conf.trailers:
            data.append(self._trailers(self.conf.trailers, offset))

        return '\n'.join(i for i in data if i is not None)

    def get_padding(self, field, offset):
        alignment = field.alignment
        padding = 0
        if alignment:
            padding = (alignment - offset) % alignment
            if padding >= alignment:
                padding = 0
        return offset + padding

    def _trailers(self, rules, offset):
        """Add code for handling of trailers to the protocol."""
        data = ['\n\t-- Trailers handling for struct: %s' % self.name]

        # Offset variable and variable declaration
        off_var = 'trail_offset'
        t_offset = '\tlocal {var} = {offset}'
        data.append(t_offset.format(offset=offset, var=off_var))

        for i, rule in enumerate(rules):
            # Find the count
            if rule.member is not None:
                # Find offset, size and func_type
                fields = [i for i in self.fields if i.name == rule.member]
                if not fields:
                    continue # rule.member don't exists in the struct
                func = fields[0].func_type

                count = 'trail_count'
                t = '\tlocal {var} = buffer({off}, {size}):{func}()'
                data.append(t.format(off=fields[0].offset,
                                 var=count, size=fields[0].size, func=func))
            else:
                count = rule.count

            size_str = ''
            if rule.size is not None:
                size_str = ', %i' % rule.size

            # Call trailers 'count' times
            tabs = '\t'
            if rule.member is not None or count > 1:
                data.append('\tfor i = 1, {count} do'.format(count=count))
                tabs += '\t'

            t1 = '{tabs}local trailer = Dissector.get("{name}")'
            t2 = '{tabs}trailer:call(buffer({off}{size}):tvb(), pinfo, tree)'
            t3 = '{tabs}{var} = {var} + {size}'
            data.append(t1.format(tabs=tabs, name=rule.name))
            data.append(t2.format(tabs=tabs, off=off_var, size=size_str))

            # Update offset after all but last trailer
            if i < len(rules)-1:
                data.append(t3.format(tabs=tabs,
                                           var=off_var, size=rule.size))

            if rule.member is not None or count > 1:
                data.append('\tend') # End for loop

        return '\n'.join(i for i in data if i is not None)


class UnionDissector(Dissector):
    def __init__(self, proto, endian):
        super().__init__(proto, endian)
        self._increase_offset = False

    @property
    def size(self):
        """Find the size of the fields in the protocol."""
        return self.get_padding(self, max(
                [0] + [field.size for field in self.children]))


class Protocol:
    """A Protocol is a collection of fields and code.

    It's used to generate Wireshark dissectors written in Lua, for
    dissecting a packet into a set of fields with values.
    """
    REGISTER_FUNC = 'delegator_register_proto'

    def __init__(self, name, conf=None, platform=None):
        """Create a Protocol, for generating a dissector.

        'name' is the name of the Protocol to dissect
        'conf' is the configuration for this Protocol
        'platform' is the platform the dissector should run on
        """
        if platform is None:
            platform = Platform.mappings['default']

        self.name = name
        self.conf = conf
        self.platform = platform

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

        self.data = [] # List of generated content
        self.children = [] # List of dissectors

        # Different lua variables
        self.var = create_lua_var('proto_%s' % name)

    def create(self):
        """Returns all the code for dissecting this protocol."""
        for child in self.children:
            child.push_modifiers()

        # Create dissector content
        self._header_defintion()
        self._fields_definition()
        self._dissector_func()
        self._register_dissector()
        return '\n'.join(i for i in self.data if i is not None)

    def _legal_header(self):
        """Add the legal header with license info."""
        pass

    def _header_defintion(self):
        """Add the code for the header of the protocol."""
        comment = '-- Dissector for %s' % self.name
        if self.description:
            comment += ': %s' % self.description
        self.data.append(comment)

        proto = 'local {var} = Proto("{name}", "{description}")\n'
        self.data.append(proto.format(var=self.var, name=self.name,
                                      description=self.description))

    def _fields_definition(self):
        """Add code for defining the ProtoField's in the protocol."""
        self.data.append('-- ProtoField defintions for: %s' % self.name)
        decl = 'local {field_var} = {var}.fields'
        self.data.append(decl.format(field_var=self.field_var, var=self.var))
        for child in children:
            self.data.append(child.get_definition())
        self.data.append('')

    def _dissector_func(self):
        """Add the code for the dissector function for the protocol."""
        self.data.append('-- Dissector function for: %s' % self.name)
        func_diss = 'function {var}.dissector(buffer, pinfo, tree)'
        sub_tree = '\tlocal subtree = tree:{add}({var}, buffer())'
        check = '\tif pinfo.private.field_name then\n\t\t'\
            'subtree:set_text(pinfo.private.field_name .. ": {name}")'\
            '\n\t\tpinfo.private.field_name = nil\n\telse\n'\
            '\t\tpinfo.cols.info:append(" (" .. {var}.description .. ")")\n'\
            '\tend\n'

        self.data.append(func_diss.format(var=self.var))
        self.data.append(sub_tree.format(
                add=self.add_var, var=self.var))
        self.data.append(check.format(var=self.var, name=self.name))

        offset = 0
        for child in children:
            child.get_code(offset)

        self.data.append('end\n')

    def _register_dissector(self):
        """Add code for registering the dissector in the dissector table."""
        if self.id is None:
            ids = ['nil']
        else:
            ids = self.id

        for id in ids:
            self.data.append('{func}({var}, "{platform}", "{name}", {id})'.format(
                    func=self.REGISTER_FUNC, var=self.var, name=self.name,
                    platform=self.platform.name, id=id))
        self.data.append('')


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
        name = 'luastructs'

        super().__init__(name, None, Platform.mappings['default'])

        self.longname = name
        self.description = 'Lua C Structs'
        self.id = None

        self.var = create_lua_var('delegator')
        self.table_var = create_lua_var('dissector_table')
        self.id_table = create_lua_var('message_ids')
        self.msg_var = create_lua_var('msg_node')

        # Add fields, don't change sizes!
        endian = Platform.big
        self.add_field(Field('Version', 'uint8', 1, 0, endian))

        values = {p.flag: p.name for name, p in self.platforms.items()}
        field = Field('Flags', 'uint8', 1, 0, endian)
        field.set_list_validation(values)
        self.add_field(field)
        self.add_field(Field('Message', 'uint16', 2, 0, endian))
        self.add_field(Field('Message length', 'uint32', 4, 0, endian))
        self._version, self._flags, self._msg_id, self._length = self.fields

    def create(self):
        """Returns all the code for dissecting this protocol."""
        self.push_modifiers()
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
        t = 'local {var} = DissectorTable.new("{name}", "Lua Structs", ftypes.STRING)'
        self.data.append(t.format(var=self.table_var, name=self.name))

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
        msg_var = create_lua_var('id_value')
        self.data.append(self._msg_id._store_value(msg_var))

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
        self.data.append(t.format(
                flags=self._flags.values, msg=msg_var, table=self.table_var,
                flag=self._flags._value_var, ids=self.id_table))

