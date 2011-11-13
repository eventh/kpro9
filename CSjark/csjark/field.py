"""
TODO
"""
import string
import copy
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


class BaseField:
    """Interface for Fields and list of Fields."""

    def __init__(self, size, alignment, endian):
        """Create a new Wireshark ProtoField instance.

        'size' the size of the field in bytes
        'alignment' the alignment of the field in bytes
        'endian' the endianess of the platform
        """
        self.size = size
        self.alignment = alignment
        self.endian = endian

    @property
    def add_var(self):
        """Get the endian specific function for adding a item to a tree."""
        if self.endian == Platform.little:
            return 'add_le'
        return 'add'

    def push_modifiers(self):
        """Push prefixes and postfixes down to child fields."""
        pass

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        pass

    def get_code(self, offset, store=None, tree='subtree'):
        """Get the code for dissecting this field."""
        pass


class ProtoTree(BaseField):
    pass


class Field(BaseField):
    """Represents Wireshark's ProtoFields which stores a specific value."""

    # Members this fields holds, used when testing equality and more
    prefixes = ['var_prefix', 'abbr_prefix', 'name_prefix']
    postfixes = ['name_postfix', 'var_postfix', 'abbr_postfix']
    infixes = ['_name', '_var', '_abbr']
    members = [
            'type', 'size', 'alignment', 'endian',
            'base', 'values', 'mask', 'desc',
            'offset', 'range_validation', 'list_validation',
    ] + prefixes + postfixes + infixes

    def __init__(self, name, type, size, alignment, endian):
        """Create a new Wireshark ProtoField instance.

        'name' the name of the field
        'type' the ProtoField type
        'size' the size of the field in bytes
        'alignment' the alignment of the field in bytes
        'endian' the endianess of the platform
        """
        for member in self.members:
            setattr(self, member, None)
        for member in self.prefixes + self.postfixes:
            setattr(self, member, [])
        super().__init__(size, alignment, endian)
        self.type = type
        self.name = name

    @property
    def name(self):
        """Get the name of the field."""
        name = self._name
        if self.name_prefix:
            name = '%s%s' % (''.join(self.name_prefix), name)
        if self.name_postfix:
            name = '%s%s' % (name, ''.join(self.name_postfix))
        return name

    @name.setter
    def name(self, value):
        """Set the infix part of the name to 'value'."""
        self._name = value
        self._var = create_lua_var(self._name)
        self._abbr = self._name.replace(' ', '_')

    @property
    def abbr(self):
        """Get the fields abbr."""
        abbr = self._abbr
        if self.abbr_prefix:
            abbr = '%s.%s' % ('.'.join(self.abbr_prefix), abbr)
        if self.abbr_postfix:
            abbr = '%s.%s' % (abbr, '.'.join(self.abbr_postfix))
        return abbr

    @property
    def variable(self):
        """Get the variable to store the field in."""
        var = self._var
        if self.var_prefix:
            var = '%s_%s' % ('_'.join(self.var_prefix), var)
        if self.var_postfix:
            var = '%s_%s' % (var, '_'.join(self.var_postfix))
        return var.replace('._', '.')

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
        if not isinstance(other, Field):
            return False
        for member in members:
            if getattr(self, member) != getattr(other, member):
                return False
        return True

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
            store = '%s_node' % self._name
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
            data.append(self._store_value()) # Store value first
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

        store = '\tlocal {var} = buffer({offset}, {size}):{type}()'
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
                            field._value_var, test, value,
                            field._node_var, warn, value)

        min, max = self.range_validation
        data = []
        if min is not None:
            data.append(create_test(self, min, '<', 'larger than'))
        if max is not None:
            data.append(create_test(self, max, '>', 'smaller than'))
        return '\n'.join(data)

    def set_list_validation(self, values, strict=True):
        """Set validating that field value is a member of 'values'."""
        if not strict:
            self.values = create_lua_valuestring(values)
            return

        self.values = create_lua_var('%s_valuestring' % self._name)
        self._valuestring_values = create_lua_valuestring(values)
        self.list_validation = ', '.join(str(i) for i in sorted(values.keys()))

    def _create_list_validation(self):
        """Create code which validates fields value in valuestring."""
        return '\tif (%s[%s] == nil) then\n\t\t%s:add_expert_info('\
                'PI_MALFORMED, PI_WARN, "Should be in [%s]")\n\tend' % (
                        self.values, self._value_var,
                        self._node_var, self.list_validation)


class Subtree(Field):
    """A Subtree is a Field with a list of fields as children."""

    def __init__(self, tree, *args, **vargs):
        """Create a new subtree of ProtoField's."""
        super().__init__(*args, **vargs)
        self.tree = tree
        self.parent = 'subtree'
        self.children = []

        # Union and bitstrings don't want each field to increase offset
        self._increase_offset = True

    def __eq__(self, other):
        """Compare if two Subtree instances are equal."""
        if (not isinstance(other, Subtree) or self.tree != other.tree or
                self._increase_offset != other._increase_offset or
                self.children != other.children):
            return False
        return True

    def push_modifiers(self, push_children=True):
        """Push prefixes and postfixes down to child fields."""
        for field in self.children:
            for member in self.prefixes + self.postfixes:
                setattr(field, member,
                        getattr(self, member) + getattr(field, member))
            if push_children:
                field.push_modifiers()

    def get_definition(self):
        """Get the ProtoField definition for this field."""
        data = [super().get_definition()]
        for field in self.children:
            data.append(field.get_definition())
        return '\n'.join(i for i in data if i is not None)

    def get_code(self, offset, store=None, tree=None):
        """Get the code for dissecting this field.

        'offset' is the buffer offset the value is stored at
        'store' is the lua variable to store the tree node in
        'tree' is the tree we are adding the node to
        """
        parent = self.parent if tree is None else tree
        tree = self.tree if store is None else store
        data = [super().get_code(offset, store=tree, tree=parent)]
        for field in self.children:
            data.append(field.get_code(offset, tree=tree))
            if self._increase_offset:
                offset += field.size
        return '\n'.join(data)


class ArrayField(Subtree):
    """ArrayField is a Subtree with visible indices."""

    def __init__(self, children, tree='arrtree', parent='subtree'):
        """Create a new ArrayField instance.

        'children' is a list of child fields
        'tree' is the variable name of the tree node
        'parent' is the variable name of the parent node
        """
        field = children[0]
        type = field.type
        if type not in ('string', 'stringz'):
            type = 'bytes'
        size = len(children) * field.size
        super().__init__(tree, field.name, type, size, 0, field.endian)
        self.parent = parent
        self.children = children

    def push_modifiers(self):
        """Push prefixes and postfixes down to child fields."""
        super().push_modifiers(push_children=False)
        for i, field in enumerate(self.children):
            field.var_postfix.append(str(i))
            field.abbr_postfix.append(str(i))
            field.name_postfix.append('[%i]' % i)
            field.push_modifiers()

    @classmethod
    def create(cls, depth, field, name='array'):
        """Recursively create a tree of arrays of 'depth'."""
        depth = depth[:]
        children = []
        for i in range(depth.pop(0)):
            if not len(depth):
                children.append(copy.deepcopy(field))
            else:
                children.append(cls.create(depth, field, 'sub%s' % name))
        return ArrayField(children, tree=name)


class BitField(Subtree):
    """BitField is a Subtree with field for each relevant bit."""

    def __init__(self, bits, name, type, size, alignment, endian):
        """Create a new BitField instance.

        'bits' is a list of relevant bits to display.
        """
        # Convert type to unsigned if int
        if 'int' in type and not type.startswith('u'):
            type = 'u%s' % type

        # Create bitstring tree field
        super().__init__('bittree', name, type, size, alignment, endian)
        self.base = 'base.HEX'

        # Create fields
        for i, j, name, values in bits:
            field = Field(name, type, size, alignment, endian)
            field.abbr_prefix.append(self.name)
            field.var_prefix.append(self.variable)
            field.values = create_lua_valuestring(values)

            # Create a mask for the bits
            tmp = [0] * self.size * 8
            for k in range(j):
                tmp[-(i+k)] = 1
            field.mask = '0x%x' % int(''.join(str(i) for i in tmp), 2)

            self.children.append(field)

        self._name = '%s (bitstring)' % self.name
        self._increase_offset = False


class ProtocolField(Field):

    def __init__(self, name, proto):
        super().__init__(name, proto.name, proto.size,
                         proto.alignment, proto.endian)
        self.proto = proto

    def get_definition(self):
        pass

    def get_code(self, offset, store=None, tree='subtree'):
        self.offset = offset
        t = '\tpinfo.private.field_name = "{name}"\n'\
            '\tDissector.get("{proto}"):call(buffer({offset}, '\
            '{size}):tvb(), pinfo, {tree})'
        return t.format(name=self.name, proto=self.proto.longname,
                offset=offset, size=self.size, tree=tree)


if __name__ == '__main__':
    print("testing")
    '''
    f = Field('enum', 'int32', 4, 0, Platform.little)
    f.var_prefix = 'f.'
    f.name_postfix = '.what?'
    f.abbr_prefix = 'swead'
    f.set_list_validation(dict(enumerate('ABCDE')))
    f.set_range_validation(5, 15)
    print(f.get_definition())
    print(f.get_code(12))
    '''
    bits = [(1, 1, 'R', {0: 'No', 1: 'Yes'}),
            (2, 1, 'B', {0: 'No', 1: 'Yes'}),
            (3, 1, 'G', {0: 'No', 1: 'Yes'})]
    f = BitField(bits, 'bitname', 'int32', 4, 4, Platform.little)
    f.var_prefix.append('f.')
    f.push_modifiers()
    print(f.get_definition())
    print(f.get_code(12))
    f = Field('arr', 'float', 4, 0, Platform.big)
    arr = ArrayField.create([2, 2, 3], f)
    arr.var_prefix.append('f.')
    arr.push_modifiers()
    print(arr.get_definition())
    print(arr.get_code(12))

