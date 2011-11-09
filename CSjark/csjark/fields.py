from platform import Platform


class Field:
    """Represents Wireshark's ProtoFields which stores a specific value."""

    def __init__(self, name, type, size, alignment, endian):
        """Create a new Field instance.

        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        'alignment' the alignment of the field in bytes
        'endian' the endianess of the platform
        """
        self.name = name
        self.type = type
        self.size = size
        self.alignment = alignment

        # Wireshark fields-specific additional arguments
        self.base = None # One of 'base.DEC', 'base.HEX' or 'base.OCT'
        self.values = None # Dict with the text that corresponds to the values
        self.mask = None # Integer mask of this field
        self.desc = None # Description of the field
        self.offset = None # Useful for others to access buffer(offset, size)

    def __eq__(self, other):
        """Compare if two field instances are equal."""
        return (self.name == other.name and self.type == other.type and
                self.size == other.size and self.alignment == other.alignment
                and self.endian == other.endian)

    def prepare(self, parent):
        pass

    def get_definition(self, sequence=None):
        """Get the ProtoField definition for this field."""
        var = self.var
        abbr = self.abbr
        index = ''
        if sequence is not None:
            postfix = self.get_array_postfix(sequence)
            var = '%s_%s' % (self.var, postfix)
            abbr = '%s_%s' % (abbr, postfix)
            index = self.get_array_index_postfix(sequence)
        return self._create_field(var, self.type, abbr,
                self.name + index, self.base, self.values, self.mask, self.desc)

    def get_code(self, offset, store=None, sequence=None, tree='subtree'):
        """Get the code for dissecting this field."""
        var = self.var
        set_text = ''
        if sequence is not None:
            var = '%s_%s' % (self.var, self.get_array_postfix(sequence))
        if store:
            store = 'local {var} = '.format(var=create_lua_var(store))
        else:
            store = ''
        self.offset = offset
        t = '\t{store}{tree}:{add}({var}, buffer({offset}, {size}))'

        return t.format(store=store, tree=tree, add=self.add_var,
                        var=var, offset=offset, size=self.size)

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

    def _tree_add(self):
        """Get the endian specific function for adding a item to a tree."""
        if self.endian == Platform.little:
            return 'add_le'
        return 'add'

    def _get_func_type(self):
        """Get the lua function to read values from buffers."""
        func_type = self.type
        if func_type[-1] == '8':
            func_type = func_type[:-1]
        if func_type[-2:] in ('16', '32'):
            func_type = func_type[:-2]

        # Endian handling
        if func_type not in ('bytes', 'string', 'stringz', 'ether'):
            if self.endian == Platform.little:
                func_type = 'le_%s' % func_type

        return func_type

    def get_padded_offset(self, offset):
        padding = 0
        if self.alignment:
            padding = self.alignment - offset % self.alignment
            if padding >= self.alignment:
                padding = 0
        return offset + padding

