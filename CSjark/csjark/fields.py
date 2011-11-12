
from platform import Platform
from dissector import create_lua_var, create_lua_valuestring


class Field:
    """Represents Wireshark's ProtoFields which stores a specific value."""
    # Members this fields holds, used when testing equality and more
    members = (
            '_name', '_var', '_abbr',
            'type', 'size', 'alignment', 'endian',
            'base', 'values', 'mask', 'desc',
            'name_prefix', 'name_postfix', 'var_prefix',
            'var_postfix', 'abbr_prefix', 'abbr_postfix',
            'validations',
    )

    def __init__(self, name, type, size, alignment, endian):
        """Create a new Field instance.

        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        'alignment' the alignment of the field in bytes
        'endian' the endianess of the platform
        """
        for member in self.members:
            setattr(self, member, None)

        self._name = name
        self._var = create_lua_var(name)
        self._abbr = name.replace(' ', '_')

        self.type = type
        self.size = size
        self.alignment = alignment
        self.endian = endian

        self.validations = [] # Keeps a list of validation code to append
        self.offset = None # Useful for others to access buffer(offset, size)

    @property
    def name(self):
        """Get the name of the field."""
        name = self._name
        name = self.name_prefix + name if self.name_prefix else name
        name = name + self.name_postfix if self.name_postfix else name
        return name

    @property
    def abbr(self):
        """Get the fields abbr."""
        abbr = self._abbr
        abbr = self.abbr_prefix + abbr if self.abbr_prefix else abbr
        abbr = abbr + self.abbr_postfix if self.abbr_postfix else abbr
        return abbr

    @property
    def abbr(self):
        """Get the variable to store the field in."""
        var = self._var
        var = self.var_prefix + var if self.var_prefix else var
        var = var + self.var_postfix if self.var_postfix else var
        return var

    @property
    def add_var(self):
        """Get the endian specific function for adding a item to a tree."""
        if self.endian == Platform.little:
            return 'add_le'
        return 'add'

    @property
    def func_type(self):
        """Get the lua function to read values from buffers."""
        func_type = self.type
        if func_type[-1] == '8':
            func_type = func_type[:-1]
        if func_type[-2:] in ('16', '32'):
            func_type = func_type[:-2]
        if func_type not in ('bytes', 'string', 'stringz', 'ether'):
            if self.endian == Platform.little:
                func_type = 'le_%s' % func_type
        return func_type

    def __eq__(self, other):
        """Compare if two field instances are equal."""
        for member in members:
            if getattr(self, member) != getattr(other, member):
                return False
        return True

    def update(self, **args):
        """Update some member values."""
        for key, value in args:
            if key in self.members and value is not None:
                setattr(self, key, value)

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        template = '{var} = ProtoField.{type}("{abbr}", "{name}"{rest})'
        args = {'var': self.var, 'type': self.type,
                'abbr': self.abbr, 'name': self.name}

        # Add other parameters if applicable
        desc = '"%s"' % self.desc if self.desc is not None else None
        other = []
        for var in reversed([self.base, self.values, self.mask, desc]):
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

    def get_code(self, offset, store=None, tree='subtree'):
        """Get the code for dissecting this field.

        'offset' is the buffer offset the value is stored at
        'store' is the lua variable to store the tree node in
        'tree' is the tree we are adding the node to
        """
        self.offset = offset
        if store:
            store = 'local {var} = '.format(var=create_lua_var(store))
        else:
            store = ''
        t = '\t{store}{tree}:{add}({var}, buffer({offset}, {size}))'
        return t.format(store=store, tree=tree, add=self.add_var,
                        var=self.var, offset=offset, size=self.size)

    def store_value(self, var, offset=None):
        """Create code which stores the field value in 'var'.

        If 'offset' is not provided, must be run after get_code().
        """
        if offset is None:
            offset = self.offset
        self._store_value_var = create_lua_var(var)
        store = 'local {var} = buffer({offset}, {size}):{type}()'
        return store.format(var=self._store_value_var, offset=offset,
                            size=self.size, type=self.func_type)

    def add_range_validation(self, min=None, max=None):
        pass

    def add_list_validation(self, valid_values):
        pass

    def get_padded_offset(self, offset):
        """TODO: move this to where its actually used."""
        padding = 0
        if self.alignment:
            padding = self.alignment - offset % self.alignment
            if padding >= self.alignment:
                padding = 0
        return offset + padding

