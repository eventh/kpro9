"""
A module which holds platform specific configuration and support
for creating dissectors for messages which originates from various
platforms.
"""


# Default mapping of C type and their wireshark field type.
DEFAULT_C_TYPE_MAP = {
        'bool': 'bool',
        'char': 'string',
        'signed char': 'string',
        'unsigned char': 'string',
        'short': "int16",
        'signed short': "int16",
        'unsigned short': "uint16",
        'short int': "int16",
        'signed short int': "int16",
        'unsigned short int': "uint16",
        "int": "int32",
        'signed int': "int32",
        'unsigned int': "uint32",
        'signed': "int32",
        'long': "int64",
        'signed long': "int64",
        'unsigned long': "uint64",
        'long int': "int64",
        'signed long int': "int64",
        'unsigned long int': "uint64",
        'long long': "int64",
        'signed long long': "int64",
        'unsigned long long': "uint64",
        'long long int': "int64",
        'signed long long int': "int64",
        'unsigned long long int': "uint64",
        'float': 'float',
        'double': 'double',
        'pointer': 'int32',
        'enum': 'uint32',
        'time_t': 'relative_time',
}


# Default mapping of C type and their default size in bytes.
DEFAULT_C_SIZE_MAP = {
        'bool': 1,
        'char': 1,
        'signed char': 1,
        'unsigned char': 1,
        'short': 2,
        'signed short': 2,
        'unsigned short': 2,
        'short int': 2,
        'signed short int': 2,
        'unsigned short int': 2,
        'int': 4,
        'signed int': 4,
        'unsigned int': 4,
        'signed': 4,
        'long': 8,
        'signed long': 8,
        'unsigned long': 8,
        'long int': 8,
        'signed long int': 8,
        'unsigned long int': 8,
        'long long': 8,
        'signed long long': 8,
        'unsigned long long': 8,
        'long long int': 8,
        'signed long long int': 8,
        'unsigned long long int': 8,
        'float': 4,
        'double': 8,
        'long double': 16,
        'pointer': 4,
        'enum': 4,
        'time_t': 4,
}


def map_type(ctype):
    """Find the wireshark type for a ctype."""
    return DEFAULT_C_TYPE_MAP.get(ctype, ctype)


def size_of(ctype):
    """Find the size of a c type in bytes."""
    if ctype in DEFAULT_C_SIZE_MAP.keys():
        return DEFAULT_C_SIZE_MAP[ctype]
    else:
        raise ValueError('No known size for type %s' % ctype)


class Platform:
    """."""
    big = 'big'
    little = 'little'
    mappings = {} # Map platform name to instance

    def __init__(self, name, flag, endian,
                 macros=None, sizes=None, alignment=4):
        if macros is None:
            macros = []
        if sizes is None:
            sizes = {}
        Platform.mappings[name] = self
        self.name = name
        self.flag = flag
        self.endian = endian
        self.macros = macros
        self.sizes = sizes
        self.alignment = alignment

        # Extend sizes with missing types from default size map
        for key, value in DEFAULT_C_SIZE_MAP.items():
            if key not in self.sizes:
                self.sizes[key] = value


# Register platforms
#Platform('win32', 0, Platform.big, ['win32', '_win32'])
#Platform('win64', 1, Platform.big)

