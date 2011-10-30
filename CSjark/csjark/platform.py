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

    def __init__(self, name, flag, endian,
                macros=None, sizes=None, alignment=None):
        """Create a configuration for a specific platform.

        'name' is the name of the platform
        'flag' is an unique integer value representing this platform
        'endian' is either Platform.big or Platform.little
        'macros' is C preprocessor platform-specific macros like _WIN32
        'sizes' is a dict which maps C types to their size in bytes
        """
        if macros is None:
            macros = {}
        if sizes is None:
            sizes = {}
        if alignment is None:
            alignment = {}
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

        for key, value in alignment.items():
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
            data.extend(generate(i) for i, j in p.macros.items())
        return '\n'.join(data)

    def _generate_defines(self):
        """Create macros which defines platform specific macros."""
        t = '\n/* Define platform-specific macros for %s */\n' % self.name
        macros = ['#define %s %s' % (i, j) for i, j in self.macros.items()]
        return t + '\n'.join(macros)


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

# Mapping of C sizes for unix like platforms
UNIX_C_SIZE_MAP = {
        'long': 8,
        'long int': 8,
        'signed long': 8,
        'signed long int': 8,
        'unsigned long': 8,
        'unsigned long int': 8,
        'long double': 16,
}

# Mapping of C sizes for sparc platform
SPARC_C_SIZE_MAP = {
        'long double': 16,
}

# Mapping of C sizes for unix like platforms
UNIX_C_ALIGNMENT_SIZE_MAP = {
        'long': 8,
        'long int': 8,
        'signed long': 8,
        'signed long int': 8,
        'unsigned long': 8,
        'unsigned long int': 8,
        'double': 16,
}

# Platform-specific C preprocessor macros
WIN32_MACROS = {
        '_WIN32': 1, '__WIN32__': 1, '__TOS_WIN__': 1,
        '__WINDOWS__': 1, 'MAX_PATH': 260,
}

SOLARIS_MACROS = {'sun': 1, '__sun': 1, 'PATH_MAX': 4096}

MACOS_MACROS = {
    'macintosh': 1, 'Macintosh': 1,
    '__APPLE__': 1, '__MACH__': 1, 'PATH_MAX': 4096,
}

X86_MACROS = {
        'i386': 1, '__i386__': 1, '__i386': 1, '__IA32__': 1,
        '_M_IX86': 1, '__X86__': 1, '_X86_': 1, '__THW_INTEL__': 1,
        '__I86__': 1, '__INTEL__': 1,
}

X64_MACROS = {
        '__amd64__': 1, '__amd64': 1, '__x86_64': 1, '__x86_64__': 1,
        '_M_X64': 1, '__ia64__': 1, '_IA64': 1, '__IA64__': 1,
        '__ia64': 1, '_M_IA64': 1, '_M_IA64': 1, '__itanium__': 1,
        '__x86_64': 1, '__x86_64__': 1, '_M_AMD64': 1,
}

SPARC_MACROS = {
        '__sparc__': 1, '__sparc': 1, '__sparcv8': 1,
        '__sparcv9': 1, 'PATH_MAX': 1024,
}


# Register different platforms
def merge(a, *dicts):
    new = dict(a)
    for d in dicts:
        new.update(d)
    return new

# Default platform
Platform('default', 0, Platform.big,
         macros={'PATH_MAX': 4096, 'MAX_PATH': 260})

# Windows 32 bit
Platform('Win32', 1, Platform.little,
         macros=merge(WIN32_MACROS, X86_MACROS),
         alignment=DEFAULT_C_ALIGNEMT_SIZE_MAP)

# Windows 64 bit
Platform('Win64', 2, Platform.little,
         macros=merge(WIN32_MACROS, X64_MACROS, {'_WIN64':1}))

# Solaris 32 bit
Platform('Solaris-x86', 3, Platform.little,
         macros=merge(SOLARIS_MACROS, X86_MACROS), sizes=UNIX_C_SIZE_MAP,
         alignment=UNIX_C_ALIGNMENT_SIZE_MAP)

# Solaris 64 bit
Platform('Solaris-x86-64', 4, Platform.little,
         macros=merge(SOLARIS_MACROS, X64_MACROS), sizes=UNIX_C_SIZE_MAP)

# Solaris SPARC 64 bit
Platform('Solaris-sparc', 5, Platform.big,
         macros=merge(SOLARIS_MACROS, SPARC_MACROS), sizes=SPARC_C_SIZE_MAP,
         alignment=SPARC_C_SIZE_MAP)

# MacOS
Platform('Macos', 6, Platform.little,
         macros=MACOS_MACROS, sizes=UNIX_C_SIZE_MAP,
         alignment=UNIX_C_ALIGNMENT_SIZE_MAP)

# Linux
Platform('Linux-x86', 7, Platform.little,
         macros={'__linux__': 1, 'PATH_MAX': 4096},
         sizes=UNIX_C_SIZE_MAP,
         alignment=UNIX_C_ALIGNMENT_SIZE_MAP)

