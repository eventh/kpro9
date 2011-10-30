"""
A module which holds platform specific configuration.

It holds the Platform class which holds specific configuration
for one platform, and a list of all supported platforms.

It is used when creating dissectors for messages which can originate
from various platforms.
"""


class Platform:
    """Represents specific attributes of an OS and/or hardware."""
    big = 'big'
    little = 'little'

    mappings = {} # Map platform name to instance

    def __init__(self, name, flag, endian, macros=None, sizes=None, alignment_sizes=None):
        """Create a configuration for a specific platform.

        'name' is the name of the platform
        'flag' is an unique integer value representing this platform
        'endian' is either Platform.big or Platform.little
        'macros' is C preprocessor platform-specific macros like _WIN32
        'sizes' is a dict which maps C types to their size in bytes
        """
        if macros is None:
            macros = []
        if sizes is None:
            sizes = {}
        if alignment_sizes is None:
            alignment_sizes = {}
        Platform.mappings[name] = self
        self.name = name
        self.flag = flag
        self.endian = endian
        self.macros = macros
        self.header = None
        self.types = dict(DEFAULT_C_TYPE_MAP)

        # Extend sizes with missing types from default size map
        self.sizes = dict(DEFAULT_C_SIZE_MAP)

        for key, value in sizes.items():
            self.sizes[key] = value

        # Extend alignment sizes with missing types from default alignment size map
        self.alignment_sizes = dict(DEFAULT_C_ALIGNEMT_SIZE_MAP)

        for key, value in alignment_sizes.items():
            self.alignment_sizes[key] = value

    def map_type(self, ctype):
        """Find the Wireshark type for a ctype."""
        if ctype in self.types:
            return self.types[ctype]
        if ctype in self.sizes:
            return 'bytes' # Default to bytes array
        raise ValueError('No known wireshark field type for ctype %s' % ctype)

    def size_of(self, ctype):
        """Find the size of a C type in bytes."""
        if ctype in self.sizes:
            return self.sizes[ctype]
        raise ValueError('No known wireshark field size for type %s' % ctype)

    def alignment_size_of(self, ctype):
        """Find the alignment size of a C type in bytes."""
        if ctype in self.alignment_sizes.keys():
            return self.alignment_sizes[ctype]
        else:
            raise ValueError('No known alignment size for type %s' % ctype)

    @classmethod
    def create_all_headers(cls):
        """Create all header macros for all platforms."""
        platforms = cls.mappings.values()
        undefs = cls._generate_undefines(platforms)
        for p in platforms:
            p.header = '%s\n%s\n' % (undefs, p._generate_defines())

    @classmethod
    def _generate_undefines(cls, platforms):
        """Create macros which undefines platform specific macros."""
        def generate(macro):
            return '#ifdef %s\n\t#undef %s\n#endif' % (macro, macro)

        data = ['/* Undefine all platform macros */']
        for p in platforms:
            data.extend(generate(i) for i in p.macros)
        return '\n'.join(data)

    def _generate_defines(self):
        """Create macros which defines platform specific macros."""
        t = '\n/* Define platform-specific macros for %s */\n' % self.name
        return t + '\n'.join(['#define %s 1' % i for i in self.macros])


# Default mapping of C type and their wireshark field type.
DEFAULT_C_TYPE_MAP = {
        'bool': 'bool',
        '_Bool': 'bool',
        'char': 'string',
        'signed char': 'string',
        'unsigned char': 'string',
        'string': 'string',
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
        '_Bool': 1,
        'char': 1,
        'signed char': 1,
        'unsigned char': 1,
        'short': 2,
        'short int': 2,
        'signed short': 2,
        'signed short int': 2,
        'unsigned short': 2,
        'unsigned short int': 2,
        'int': 4,
        'signed': 4,
        'signed int': 4,
        'unsigned': 4,
        'unsigned int': 4,
        'long': 4,
        'long int': 4,
        'signed long': 4,
        'signed long int': 4,
        'unsigned long': 4,
        'unsigned long int': 4,
        'long long': 8,
        'long long int': 8,
        'signed long long': 8,
        'signed long long int': 8,
        'unsigned long long': 8,
        'unsigned long long int': 8,
        'float': 4,
        'double': 8,
        'long double': 8,
        'pointer': 4,
        'enum': 4,
        'time_t': 4,
}


# Default mapping of C type and their default size in bytes.
DEFAULT_C_ALIGNEMT_SIZE_MAP = {
        'bool': 0,
        '_Bool': 0,
        'char': 0,
        'signed char': 0,
        'unsigned char': 0,
        'short': 0,
        'short int': 0,
        'signed short': 0,
        'signed short int': 0,
        'unsigned short': 0,
        'unsigned short int': 0,
        'int': 0,
        'signed': 0,
        'signed int': 0,
        'unsigned': 0,
        'unsigned int': 0,
        'long': 0,
        'long int': 0,
        'signed long': 0,
        'signed long int': 0,
        'unsigned long': 0,
        'unsigned long int': 0,
        'long long': 0,
        'long long int': 0,
        'signed long long': 0,
        'signed long long int': 0,
        'unsigned long long': 0,
        'unsigned long long int': 0,
        'float': 0,
        'double': 0,
        'long double': 0,
        'pointer': 0,
        'enum': 0,
        'time_t': 0,
}


# Mapping of C sizes for unix like platforms
UNIX_C_SIZE_MAP = {
        'long': 8,
        'long int': 8,
        'signed long': 8,
        'signed long int': 8,
        'unsigned long': 8,
        'unsigned long int': 8,
}


# Mapping of C sizes for unix like platforms
UNIX_C_ALIGNMENT_SIZE_MAP = {
        'double': 0,
}


# Platform-specific C preprocessor macros
WIN32_MACROS = ['_WIN32', '__WIN32__', '__TOS_WIN__', '__WINDOWS__']
SOLARIS_MACROS = ['sun', '__sun']
MACOS_MACROS = ['macintosh', 'Macintosh', '__APPLE__', '__MACH__']

X86_MACROS = [
    'i386', '__i386__', '__i386', '__IA32__', '_M_IX86', '__X86__',
    '_X86_', '__THW_INTEL__', '__I86__', '__INTEL__',
]

X64_MACROS = [
    '__amd64__', '__amd64', '__x86_64', '__x86_64__', '_M_X64',
    '__ia64__', '_IA64', '__IA64__', '__ia64', '_M_IA64', '_M_IA64',
    '__itanium__', '__x86_64', '__x86_64__', '_M_AMD64',
]

SPARC_MACROS = ['__sparc__', '__sparc', '__sparcv8', '__sparcv9']


# Register different platforms

# Default platform
Platform('default', 0, Platform.big)

# Windows 32 bit
Platform('Win32', 1, Platform.little, macros=WIN32_MACROS+X86_MACROS,
         alignment_sizes=DEFAULT_C_SIZE_MAP)

# Windows 64 bit
Platform('Win64', 2, Platform.little,
         macros=WIN32_MACROS+X64_MACROS+['_WIN64'])

# Solaris 32 bit
Platform('Solaris-x86', 3, Platform.little,
         macros=SOLARIS_MACROS+X86_MACROS, sizes=UNIX_C_SIZE_MAP,
         alignment_sizes=UNIX_C_ALIGNMENT_SIZE_MAP)

# Solaris 64 bit
Platform('Solaris-x86-64', 4, Platform.little,
         macros=SOLARIS_MACROS+X64_MACROS, sizes=UNIX_C_SIZE_MAP)

# Solaris SPARC 64 bit
Platform('Solaris-sparc', 5, Platform.big,
         macros=SOLARIS_MACROS+SPARC_MACROS, sizes=UNIX_C_SIZE_MAP)

# MacOS
Platform('Macos', 6, Platform.little,
         macros=MACOS_MACROS, sizes=UNIX_C_SIZE_MAP,
         alignment_sizes=UNIX_C_ALIGNMENT_SIZE_MAP)

# Linux
Platform('Linux-x86', 7, Platform.little,
         macros=['__linux__'], sizes=UNIX_C_SIZE_MAP,
         alignment_sizes=UNIX_C_ALIGNMENT_SIZE_MAP)

