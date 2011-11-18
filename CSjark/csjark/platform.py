# -*- coding: utf-8 -*-
# Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
# Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
# Sigurd Wien and Jaroslav Fibichr.
#
# This file is part of CSjark.
#
# CSjark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSjark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSjark.  If not, see <http://www.gnu.org/licenses/>.
"""
A module which holds platform specific configuration.

It holds the Platform class which holds specific configuration
for one platform, and a list of all supported platforms.

It is used when creating dissectors for messages which can originate
from various platforms.
"""


class Platform:
    """Represents specific attributes of a platform.

    Platform here refers to a combination of Operating System,
    Hardware platform and Compiler. An instance of this class is an
    abstraction of all of these. It inceases the number of platforms
    if one wish to support many, but the utility only need to handle
    one at a time.
    """
    big = 'big'
    little = 'little'

    mappings = {} # Map platform name to instance
    flags = {} # Map platform flag to platform

    def __init__(self, name, flag, endian, macros=None,
            sizes=None, alignment=None, types=None):
        """Create a configuration for a specific platform.

        'name' is the name of the platform
        'flag' is an unique integer value representing this platform
        'endian' is either Platform.big or Platform.little
        'macros' is C preprocessor platform-specific macros like _WIN32
        'sizes' is a dict which maps C types to their size in bytes
        'alignment' is a dict which maps C types to their alignment in bytes
        'types' is a dict mapping C types to Wireshark ProtoField types
        """
        if flag in Platform.flags:
            raise Exception('%i is already used by another platform' % flag)
        if macros is None:
            macros = {}
        if sizes is None:
            sizes = {}
        if alignment is None:
            alignment = {}
        if types is None:
            types = {}
        Platform.mappings[name] = self
        Platform.flags[flag] = self
        self.flag = flag
        self.name = name
        self.endian = endian
        self.macros = macros
        self.header = None

        # Extend or overwrite type mapping from default type map
        self.types = dict(DEFAULT_C_TYPE_MAP)
        for key, value in types.items():
            self.types[key] = value

        # Extend sizes with missing types from default size map
        self.sizes = dict(DEFAULT_C_SIZE_MAP)
        for key, value in sizes.items():
            self.sizes[key] = value

        # Extend alignment sizes with missing types from default alignment size map
        self.alignments = dict(DEFAULT_C_ALIGNEMT_SIZE_MAP)
        for key, value in alignment.items():
            self.alignments[key] = value

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

    def alignment(self, ctype):
        """Find the alignment size of a C type in bytes."""
        if ctype in self.alignments:
            return self.alignments[ctype]
        raise ValueError('No known alignment size for type %s' % ctype)


# Default mapping of C type and their wireshark field type.
DEFAULT_C_TYPE_MAP = {
        'bool': 'bool',
        '_Bool': 'bool',
        'char': 'int8',
        'signed char': 'int8',
        'unsigned char': 'uint8',
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


# Default type size in bytes.
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


# Default alignment size in bytes.
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

# Custom C sizes
# Mapping of C sizes for Windows 64-bit platform
WIN64_C_SIZE_MAP = {
        'pointer': 8,
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


# Mapping of C sizes for Solaris-x86 platform
SOLARIS_X86_C_SIZE_MAP = {
        'long': 4,
        'long int': 4,
        'signed long': 4,
        'signed long int': 4,
        'unsigned long': 4,
        'unsigned long int': 4,
        'long double': 16,
}


# Mapping of C sizes for sparc platform
SPARC_C_SIZE_MAP = {
        'long double': 16,
}

# Custom alignment sizes
# Mapping of alignment sizes for unix like platforms
UNIX_C_ALIGNMENT_SIZE_MAP = {
        'long': 8,
        'long int': 8,
        'signed long': 8,
        'signed long int': 8,
        'unsigned long': 8,
        'unsigned long int': 8,
        'long double': 16,
}



# Platform-specific C preprocessor macros
WIN32_MACROS = {
        '_WIN32': 1, '__WIN32__': 1, '__TOS_WIN__': 1,
        '__WINDOWS__': 1, 'MAX_PATH': 260, 'sUNIX': 1,
}

SOLARIS_MACROS = {'sun': 1, '__sun': 1, 'PATH_MAX': 4096, 'sUNIX': 1}

MACOS_MACROS = {
    'macintosh': 1, 'Macintosh': 1, 'sUNIX': 1,
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
        '__sparc__': 1, '__sparc': 1,
        '__sparcv9': 1, 'PATH_MAX': 1024,
}


# Register different platforms
def merge(a, *dicts):
    """Merge several dictinaries into a new one."""
    new = dict(a)
    for d in dicts:
        new.update(d)
    return new


# Default platform
Platform('default', 0, Platform.big,
         macros={'sUNIX': 1, 'PATH_MAX': 4096, 'MAX_PATH': 260})

# Windows 32 bit
Platform('Win32', 1, Platform.little,
         macros=merge(WIN32_MACROS, X86_MACROS),
         alignment=DEFAULT_C_ALIGNEMT_SIZE_MAP)

# Windows 64 bit
Platform('Win64', 2, Platform.little,
         macros=merge(WIN32_MACROS, X64_MACROS, {'_WIN64': 1}),
         sizes=WIN64_C_SIZE_MAP, alignment=WIN64_C_SIZE_MAP)

# Solaris 32 bit
Platform('Solaris-x86', 3, Platform.little,
         macros=merge(SOLARIS_MACROS, X86_MACROS),
         sizes=SOLARIS_X86_C_SIZE_MAP,
         alignment=SOLARIS_X86_C_SIZE_MAP)

# Solaris 64 bit
Platform('Solaris-x86-64', 4, Platform.little,
         macros=merge(SOLARIS_MACROS, X64_MACROS),
         sizes=UNIX_C_SIZE_MAP)

# Solaris SPARC 64 bit
Platform('Solaris-sparc', 5, Platform.big,
         macros=merge(SOLARIS_MACROS, SPARC_MACROS),
         sizes=SPARC_C_SIZE_MAP,
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

