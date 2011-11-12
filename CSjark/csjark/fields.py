"""
TODO
"""
from platform import Platform
from dissector import create_lua_var


def create_lua_valuestring(dict_, wrap=True):
    """Convert a python dictionary to lua table."""
    items = dict_.items()
    if wrap:
        items = [(i, '"%s"' % j) for i, j in items]
    return '{%s}' % ', '.join('[%i]=%s' % (i, j) for i, j in items)


class Field:
    """Represents Wireshark's ProtoFields which stores a specific value."""
    # Members this fields holds, used when testing equality and more
    members = (
            '_name', '_var', '_abbr',
            'type', 'size', 'alignment', 'endian',
            'base', 'values', 'mask', 'desc',
            'name_prefix', 'name_postfix', 'var_prefix',
            'var_postfix', 'abbr_prefix', 'abbr_postfix',
            'range_validation', 'list_validation',
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
    def variable(self):
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
        data = []

        # Store the valuestring in a variable if we use it later
        if self.list_validation is not None:
            data.append('local {var} = {values}'.format(
                    var=self.values, values=self._valuestring_values))

        # Create a ProtoField defintion for the Field
        template = '{var} = ProtoField.{type}("{abbr}", "{name}"{rest})'
        args = {'var': self.variable, 'type': self.type,
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

        data.append(template.format(**args))
        return '\n'.join(data)

    def get_code(self, offset, store=None, tree='subtree'):
        """Get the code for dissecting this field.

        'offset' is the buffer offset the value is stored at
        'store' is the lua variable to store the tree node in
        'tree' is the tree we are adding the node to
        """
        self.offset = offset
        data = []

        # Store the subtree node in a lua variable
        if not store and (self.range_validation or self.list_validation):
            store = '%s_node' % self.name
        if store:
            self._node_var = create_lua_var(store)
            store = 'local {var} = '.format(var=self._node_var)
        else:
            store = ''

        # Add the field to the Wireshark tree
        t = '\t{store}{tree}:{add}({var}, buffer({offset}, {size}))'
        data.append(t.format(store=store, tree=tree, add=self.add_var,
                var=self.variable, offset=offset, size=self.size))

        # Add misc validations
        if self.range_validation or self.list_validation:
            self._store_value() # Store value first
        if self.range_validation is not None:
            data.append(self._create_range_validation())
        if self.list_validation is not None:
            data.append(self._create_list_validation())
        return '\n'.join(data)

    def _store_value(self, var=None, offset=None):
        """Create code which stores the field value in 'var'.

        If 'offset' is not provided, must be run after get_code().
        """
        if var is None:
            var = '%s_value' % self._name
        if offset is None:
            offset = self.offset
        self._value_var = create_lua_var(var)

        store = 'local {var} = buffer({offset}, {size}):{type}()'
        return store.format(var=self._value_var, offset=offset,
                            size=self.size, type=self.func_type)

    def set_range_validation(self, min_value=None, max_value=None):
        """Set validation that field value is between a given range."""
        self.range_validation = [min_value, max_value]

    def _create_range_validation(self):
        """Create code which validates the field value inside the range."""
        def create_test(field, value, test, warn):
            return '\tif (%s %s %s) then\n\t\t%s:add_expert_info('\
                    'PI_MALFORMED, PI_WARN, "Should be %s %s")\n\tend' % (
                            field._value_var, value_var, test,
                            value, field._node_var, warn, value)

        min, max = self.range_validation
        data = []
        if min is not None:
            data.append(create_test(field, min, '<', 'larger than'))
        if max is not None:
            data.append(create_test(field, max, '>', 'smaller than'))
        return '\n'.join(data)

    def set_list_validation(self, values, strict=True):
        """Set validating that field value is a member of 'values'."""
        if not strict:
            self.values = create_lua_valuestring(values)
            return

        self.values = create_lua_var('%s_valuestring' % self.name)
        self._valuestring_values = create_lua_valuestring(values)
        self.list_validation = ', '.join(str(i) for i in sorted(values.keys()))

    def _create_list_validation(self):
        """Create code which validates fields value in valuestring."""
        return '\tif (%s[%s] == nil) then\n\t\t%s:add_expert_info('\
                'PI_MALFORMED, PI_WARN, "Should be in (%s)")\n\tend' % (
                        self.values, self._value_var,
                        self._node_var, self.list_validation)

    def get_padded_offset(self, offset):
        """TODO: move this to where its actually used."""
        padding = 0
        if self.alignment:
            padding = self.alignment - offset % self.alignment
            if padding >= self.alignment:
                padding = 0
        return offset + padding


if __name__ == '__main__':
    print("testing")

