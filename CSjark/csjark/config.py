"""
A module for configuration of our utility.

Should parse config files and create data structures which the parser can
use when translating C struct definitions to Wireshark protocols and fields.
"""
import sys
import os
from operator import itemgetter

import yaml

from platform import Platform
from dissector import Delegator, create_lua_valuestring


class ConfigError(Exception):
    """Exception raised by invalid configuration."""
    pass


class Config:
    """Holds configuration for a specific protocol."""

    def __init__(self, name):
        self.name = name
        self.id = None # Message id
        self.description = None
        self.cnf = None # Conformance File, for custom lua code
        self.members = {} # Rules for struct members
        self.types = {} # Rules for struct member types
        self.trailers = [] # Rules for protocol trailers

    def add_member_rule(self, member, rule):
        if member not in self.members.keys():
            self.members[member] = []
        self.members[member].append(rule)

    def add_type_rule(self, type, rule):
        if type not in self.types.keys():
            self.types[type] = []
        self.types[type].append(rule)

    def get_rules(self, member, type):
        rules = self.members.get(member, [])
        rules.extend(self.types.get(type, []))
        return rules

    def create_field(self, proto, name, ctype, size=None, alignment=None):
        """Create a field depending on rules."""
        # Sort the rules
        types = (Bitstring, Enum, Range, Custom)
        values = [[], [], [], []]
        for rule in self.get_rules(name, ctype):
            for i, tmp in enumerate(types):
                if isinstance(rule, tmp):
                    values[i].append(rule)
        bits, enums, ranges, customs = values

        # Custom field rules
        if customs:
            return customs[0].create(proto, name, ctype, size, alignment)

        # If size is None and not customs rule, we are in trouble.
        if size is None:
            size = proto.platform.size_of(ctype)
        type_ = proto.platform.map_type(ctype)

        if alignment is None:
            raise ConfigError('Unknown field alignment for %s' % name)

        # Bitstring rules
        if bits:
            return proto.add_bit(name, type_, size, alignment, bits[0].bits)

        # Enum rules
        if enums:
            rule = enums[0]
            return proto.add_enum(name, type_, size, alignment, rule.values, rule.strict)

        # Range rules
        if ranges:
            rule = ranges[0]
            return proto.add_range(name, type_, size, alignment, rule.min, rule.max)

        # Create basic Field if no rules fired
        return proto.add_field(name, type_, size, alignment)

    def get_field_attributes(self, name, ctype):
        """Create a field depending on rules."""
        # Sort the rules
        types = (Bitstring, Enum, Range, Custom)
        values = [[], [], [], []]
        for rule in self.get_rules(name, ctype):
            for i, tmp in enumerate(types):
                if isinstance(rule, tmp):
                    values[i].append(rule)
        return values


class BaseRule:
    """A base class for rules referring to protocol fields."""

    def __init__(self, conf, obj):
        # A field rule refers either to a type or a member
        self.member = self.type = None
        if 'member' in obj:
            self.member = obj['member']
            conf.add_member_rule(self.member, self)
            del obj['member']
        elif 'type' in obj:
            self.type = obj['type']
            conf.add_type_rule(self.type, self)
            del obj['type']
        else:
            raise ConfigError('Missing either type or member declaration')


class Range(BaseRule):
    """Rule for specifying a valid range for a member or type."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)

        # Min and max represents the endpoints of the valid range
        self.min = self.max = None
        if 'min' in obj:
            self.min = float(obj['min'])
        if 'max' in obj:
            self.max = float(obj['max'])
        if self.min is None and self.max is None:
            raise ConfigError('Range rule needs a min or max value.')


class Enum(BaseRule):
    """Rule for emulating enum with int-like types."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)
        self.strict = obj.get('strict', True)

        # Values is a dict which map values to enum names
        self.values = obj.get('values', None)
        if not self.values:
            raise ConfigError('Enum needs a non-empty dict or list')
        if isinstance(self.values, (list, tuple)):
            self.values = dict(enumerate(self.values))


class Bitstring(BaseRule):
    """Rule for representing ints which are bit strings."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)

        # Find all bitstring definitions
        self.bits = []
        for key, value in obj.items():
            # Find the bits referred to by the key
            try:
                int(key)
            except ValueError:
                if '-' not in key:
                    raise ConfigError('Invalid bitstring key: %s' % key)
                start, end = [int(i) for i in key.split('-')]
                offset = end - start + 1
            else:
                start, offset = key, 1
            if not key:
                raise ConfigError('Invalid bitstring key must be %i > 0' % key)

            # Find the bit name and values mapping
            name = value
            values = {}
            if not isinstance(value, str):
                name = value[0]
                if len(value) > 1:
                    values = dict(enumerate(value[1:]))
                elif offset == 1:
                    values = {0: 'No', 1: 'Yes'}
            elif offset == 1:
                values = {0: 'No', 1: 'Yes'}

            self.bits.append((start, offset, name, values))

        self.bits.sort(key=itemgetter(0))
        if not self.bits:
            raise ConfigError('Invalid bitstring rule for %s' % conf.name)


class Trailer(BaseRule):
    """Rule for specifying one or more trailer protocol(s)."""

    def __init__(self, conf, obj):
        # Name of the dissector to call for the trailer
        self.name = str(obj['name'])
        if not self.name:
            raise ConfigError('Invalid trailer rule for %s' % conf.name)
        conf.trailers.append(self)

        # Count or member, which holds the amount of trailers
        self.count = self.member = None
        if 'count' in obj:
            self.count = int(obj['count'])
        if 'member' in obj:
            self.member = str(obj['member'])
        if ((self.count is None and not self.member) or
                (self.count is not None and self.member is not None)):
            raise ConfigError('Invalid trailer rule for %s' % conf.name)

        # Optional size a single trailing protocol
        self.size = None
        if 'size' in obj:
            self.size = int(obj['size'])


class Custom(BaseRule):
    """Rule for specifying a custom field handling."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)
        self.field = str(obj.get('field', ''))
        if not self.field:
            raise ConfigError('No field in Custom rule for %s' % conf.name)

        # TODO: validate that the parameters are valid for the field type
        self.size = obj.get('size', None)
        self.alignment = obj.get('alignment_size', None)
        self.abbr = obj.get('abbr', None)
        self.name = obj.get('name', None)
        self.base = obj.get('base', None)
        self.values = obj.get('values', None)
        self.mask = obj.get('mask', None)
        self.desc = obj.get('desc', None)

    def create(self, proto, name, ctype, size, alignment):
        if self.size is not None:
            size = self.size
        else:
            if ctype not in proto.platform.sizes:
                raise ConfigError('Missing size for field %s' % name)
            size = proto.platform.size_of(ctype)
        if self.alignment is not None:
            alignment = self.alignment
        if alignment is None:
            alignment = size
        field = proto.add_field(name, self.field, size, alignment)
        if self.abbr is not None:
            field.abbr = self.abbr
        field.base = self.base
        if self.values:
            field.values = create_lua_valuestring(self.values)
        field.mask = self.mask
        field.desc = self.desc
        return field


class ConformanceFile:
    """A class for parsing a conformance file.

    A conformance file specifies custom lua code for fields.
    It can give custom code for the defintion, and inside the dissector
    function. For these two cases, it supports header, body, footer and
    extra sections which places code above, instead of, below, or at the
    end of the section.

    Each section starts with #.<SECTION> for example #.COMMENT.
    Unknown sections are ignore, to be compatible with Asn2wrs .cnf files.
    """
    # Tokens for different sections
    t_def_hdr = 'DEF_HEADER'    # Lua code added before a field defintion
    t_def_body = 'DEF_BODY'     # Lua code to replace a field defintion
    t_def_ftr = 'DEF_FOOTER'    # Lua code added after a field defintion
    t_def_extra = 'DEF_EXTRA'   # Lua code added after all defintions
    t_func_hdr = 'FUNC_HEADER'  # Lua code added before a field function code
    t_func_body = 'FUNC_BODY'   # Lua code to replace a field function code
    t_func_ftr = 'FUNC_FOOTER'  # Lua code added after a field function code
    t_func_extra = 'FUNC_EXTRA' # Lua code added at end of dissector function
    t_comment = 'COMMENT'       # A multiline comment section
    t_end = 'END'               # End of a section
    t_end_cnf = 'END_OF_CNF'    # End of the conformance file

    # List of all valid tokens and tokens which should store content
    def_tokens = [t_def_hdr, t_def_body, t_def_ftr]
    func_tokens = [t_func_hdr, t_func_body, t_func_ftr]
    store_tokens = def_tokens + func_tokens + [t_def_extra, t_func_extra]
    valid_tokens = store_tokens + [t_comment, t_end, t_end_cnf]

    def __init__(self, conf, file, config_file=''):
        """Parse a conformance file and create rules for it."""
        # Find the specified file
        self.file = str(file)
        if not os.path.isfile(self.file):
            self.file = os.path.join(os.path.dirname(__file__), file)
        if not os.path.isfile(self.file):
            self.file = os.path.join(os.path.dirname(config_file), file)
        if not os.path.isfile(self.file):
            raise ConfigError('Unknown file: %s' % file)

        # Read content of the specified file
        with open(self.file, 'r') as f:
            self._lines = f.readlines()

        self.rules = {}
        self.parse()

    def _get_token(self, line):
        """Find the token and the field it refers to."""
        values = line[2:].strip().split(' ') + [None]
        return values[0], values[1]

    def parse(self):
        """Parse the conformance file's sections and content."""
        token = None # Current section beeing parsed
        field = None # Field the section refers to
        content = [] # Current content for the section parsed so far

        # Go through all lines and assign content
        for line in self._lines:
            if not line.startswith('#.'):
                content.append(line.rstrip())
                continue

            # Store current content when new token is found
            if token in self.store_tokens:
                self.rules[(field, token)] = '\n'.join(content)

            content = []
            token, field = self._get_token(line)

            if token == self.t_end_cnf:
                break # End of cnf file

        # Reached end of file without an end token
        if content and token in self.store_tokens:
            self.rules[(field, token)] = '\n'.join(content)

    def match(self, name, code, defintion=False):
        """Modify fields code if a cnf file demands it."""
        # Handle extra code rules
        if name is None and code is None:
            if defintion:
                token = self.t_def_extra
            else:
                token = self.t_func_extra
            return self.rules.get((name, token), '')

        if defintion:
            tokens = self.def_tokens
        else:
            tokens = self.func_tokens

        # Modify code if field match any rules, body first
        for token in sorted(tokens):
            content = self.rules.get((name, token), '')
            if not content:
                continue
            if token.endswith('_HEADER'):
                code = '%s\n%s' % (content, code)
            elif token.endswith('_FOOTER'):
                code = '%s\n%s' % (code, content)
            elif token.endswith('_BODY'):
                content = content.replace('%(DEFAULT_BODY)s', code)
                content = content.replace('{DEFAULT_BODY}', code)
                code = content

        return code


class Options:
    """Holds options for the whole utility.

    These options are set by either command line interface or
    one or more configuration yaml files.
    """
    # Parser options, can also be set by CLI
    verbose = False
    debug = False
    strict = True
    output_dir = None
    output_file = None
    generate_placeholders = False

    # C preprocessor options, can also be set by CLI
    use_cpp = True
    cpp_include_dirs = []
    cpp_includes = []
    cpp_defines = []
    cpp_undefines = []
    cpp_args = []

    # Utility options
    platforms = set() # Set of platforms to support in dissectors
    delegator = None # Used to create a delegator dissector
    configs = {} # Configuration for specific protocols
    files = {} # Configuration for specific files

    @classmethod
    def update(cls, obj):
        """Update the options from a config yaml file."""
        # Handle platform options
        if 'platforms' in obj:
            for name in obj['platforms']:
                if name in Platform.mappings:
                    cls.platforms.add(Platform.mappings[name])
                else:
                    raise ConfigError('Unknown platform %s' % name)

        # Handle boolean options
        cls.verbose = obj.get('verbose', cls.verbose)
        cls.debug = obj.get('debug', cls.debug)
        #cls.strict = obj.get('strict', cls.strict)
        cls.output_dir = obj.get('output_dir', cls.output_dir)
        cls.output_file = obj.get('output_file', cls.output_file)

        # Handle C preprocessor arguments
        cls.use_cpp = obj.get('use_cpp', cls.use_cpp)
        if 'cpp' in obj:
            cppobj = obj['cpp']
            cls.cpp_include_dirs.extend(cppobj.get('include_dirs', []))
            cls.cpp_includes.extend(cppobj.get('includes', []))
            cls.cpp_defines.extend(cppobj.get('defines', []))
            cls.cpp_undefines.extend(cppobj.get('undefines', []))
            cls.cpp_args.extend(cppobj.get('arguments', []))

    @classmethod
    def prepare_for_parsing(cls):
        """Prepare options before parsing starts.."""
        # Map current platform to a platform configuration
        if not cls.platforms:
            mapping = {'win': 'Win32', 'darwin': 'Macos', 'linux': 'Linux-x86'}
            for key, value in mapping.items():
                if sys.platform.startswith(key):
                    cls.platforms.add(Platform.mappings[value])

        # Add the default platform, as we failed the previous step
        if not cls.platforms:
            cls.platforms.add(Platform.mappings['default'])

        # Delegator creates lua file which delegates messages to dissectors
        cls.delegator = Delegator(Platform.mappings)

    @classmethod
    def handle_protocol_config(cls, obj, filename=''):
        """Handle rules and configuration for a protocol."""
        # Handle the name of the protocol
        name = str(obj.get('name', ''))
        if not name:
            raise ConfigError('Protocol in %s not named' % filename)

        if name not in cls.configs:
            cls.configs[name] = Config(name)
        conf = cls.configs[name]

        # Protocol's optional id
        if 'id' in obj:
            conf.id = int(obj['id'])
            if conf.id < 0 or conf.id > 65535:
                raise ConfigError('Invalid dissector ID %s: %i (0 - 65535)' % (
                        conf.name, conf.id))

        # Protocol's optional description
        if 'description' in obj:
            conf.description = obj['description']

        # Protocol's optional conformance file
        if 'cnf' in obj:
            conf.cnf = ConformanceFile(conf, obj['cnf'], filename)

        # Handle rules
        types = {'bitstrings': Bitstring, 'enums': Enum, 'ranges': Range,
                 'trailers': Trailer, 'customs': Custom}
        for name, type_ in types.items():
            if name in obj:
                for rule in obj[name]:
                    type_(conf, rule)


def parse_file(filename, only_text=None):
    """Parse a configuration file."""
    if only_text is not None:
        obj = yaml.safe_load(only_text)
    else:
        with open(filename, 'r') as f:
            obj = yaml.safe_load(f)

    # Deal with utility options
    options = obj.get('Options', None)
    if options:
        Options.update(options)

    # Deal with protocol configuration
    protocols = obj.get('Structs', None)
    if protocols:
        for proto in protocols:
            Options.handle_protocol_config(proto, filename)

    if Options.verbose:
        print("Parsed config file '%s' successfully." % filename)

