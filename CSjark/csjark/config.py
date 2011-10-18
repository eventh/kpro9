"""
A module for configuration of our utility.

Should parse config files and create data structures which the parser can
use when translating C struct definitions to Wireshark protocols and fields.
"""
import os
from operator import itemgetter
import yaml


# Mapping of c type and their wireshark field type.
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
        'long double': 'todo',
        'pointer': 'int32',
        'enum': 'uint32',
        'time_t': 'relative_time',
}


# Mapping of c type and their default size in bytes.
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


class ConfigError(Exception):
    """Exception raised by invalid configuration."""
    pass


class StructConfig:
    """Holds configuration for a specific struct."""
    configs = {}

    def __init__(self, name):
        StructConfig.configs[name] = self

        self.name = name
        self.id = None
        self.description = None
        self.cnf = None # Conformance File, for custom lua code
        self.members = {} # Rules for members in the struct
        self.types = {} # Rules for types in the struct
        self.trailers = [] # Rules for struct trailers

    @classmethod
    def find(cls, name):
        if name not in cls.configs.keys():
            return cls(name)
        else:
            return cls.configs[name]

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

    def create_field(self, proto, name, ctype, size=None):
        """Create a field depending on rules."""
        type_ = map_type(ctype)

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
            return customs[0].create(proto, name, type_, size, ctype)

        # If size is None and not customs rule, we are in trouble.
        if size is None:
            raise ConfigError('Unknown field size for %s' % name)

        # Bitstring rules
        if bits:
            return proto.add_bit(name, type_, size, bits[0].bits)

        # Enum rules
        if enums:
            rule = enums[0]
            return proto.add_enum(name, type_, size, rule.values, rule.strict)

        # Range rules
        if ranges:
            rule = ranges[0]
            return proto.add_range(name, type_, size, rule.min, rule.max)

        # Create basic Field if no rules fired
        return proto.add_field(name, type_, size)


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
    """Rule for specifying a valid range for a struct member or type."""

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
    """Rule for emulating enum with int-like types in structs."""

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
    """Rule for representing bit strings in structs."""

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
        self.name = str(obj['name'])
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

        if not self.name:
            raise ConfigError('Invalid trailer rule for %s' % conf.name)


class Custom(BaseRule):
    """Rule for specifying a custom field handling."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)

        # Conformance File specification for this member or type
        self.cnf = None
        if 'cnf' in obj:
            self.cnf = ConformanceFile(conf, obj['cnf'])

        # Field, optional if conformance
        self.field = str(obj.get('field', ''))
        if not self.field and self.cnf is None:
            raise ConfigError('No field in Custom rule for %s' % conf.name)

        # TODO: validate that the parameters are valid for the field type
        self.size = obj.get('size', None)
        self.abbr = obj.get('abbr', None)
        self.name = obj.get('name', None)
        self.base = obj.get('base', None)
        self.values = obj.get('values', None)
        self.mask = obj.get('mask', None)
        self.desc = obj.get('desc', None)

    def create(self, proto, name, type_, size, ctype):
        if self.size is not None:
            size = self.size
        if size is None:
            raise ConfigError('Missing size for field %s' % name)
        field = proto.add_custom(name, self.field, size, self)
        field.abbr = self.abbr
        field.base = self.base
        if self.values:
            field.values = field._dict_to_table(self.values)
        field.mask = self.mask
        field.desc = self.desc
        return field


class ConformanceFile:
    # Tokens for different sections
    t_hdr = 'FN_HDR'
    t_body = 'FN_BODY'
    t_end = 'END'
    t_end_cnf = 'END_OF_CNF'
    tokens = [t_hdr, t_body, t_end, t_end_cnf]

    def __init__(self, conf, file, rule=None):
        # Find the specified file
        self.file = str(file)
        if not os.path.isfile(self.file):
            self.file = os.path.join(os.path.dirname(__file__), self.file)
        if not os.path.isfile(self.file):
            raise ConfigError('Unknown file: %s' % file)

        # Read content of the specified file
        with open(self.file, 'r') as f:
            self._lines = f.readlines()

        # Section contents
        self.header = None
        self.body = None

        self.parse()

    def _get_token(self, line):
        tmp = line[2:].strip().split(' ')
        return tmp[0], [], {}

    def handle_body(self, content):
        if '%(DEFAULT_BODY)s' in content:
            content = content.replace('%(DEFAULT_BODY)s', '{DEFAULT_BODY}')
        self.body = content

    def handle_header(self, content):
        self.header = content

    def parse(self):
        """Parse the conformance file's sections and content."""
        token = None # Current section beeing parsed
        args = [] # Positional arguments for the handle function
        vargs = {} # Named arguments for the handle function
        content = '' # Current content for the section parsed so far

        # Maps token to function for handling its content
        mapping = {
                self.t_body: self.handle_body,
                self.t_hdr: self.handle_header,
        }

        # Go through all lines and assign content
        for line in self._lines:
            if not line.startswith('#.'):
                content += line.strip()
                continue

            # Store current content when new token is found
            if token is not None:
                if token in mapping:
                    mapping[token](content, *args, **vargs)

            content = ''
            token, args, vargs = self._get_token(line)

            if token == self.t_end_cnf:
                break # End of cnf file
            if token == self.t_end:
                continue # End token

        # Reached end of file without an end token
        if token not in (self.t_end, self.t_end_cnf):
            if token in mapping:
                mapping[token](content)
            content = ''


def handle_struct(obj):
    """Handle rules and configuration for a struct."""
    conf = StructConfig.find(obj['name'])

    # Structs optional id
    if 'id' in obj:
        conf.id = int(obj['id'])
        if conf.id < 0 or conf.id > 65535:
            raise ConfigError('Invalid dissector ID %s: %i (0 - 65535)' % (
                    conf.name, conf.id))

    # Structs optional description
    if 'description' in obj:
        conf.description = obj['description']

    # Structs optional conformance file
    if 'cnf' in obj:
        conf.cnf = ConformanceFile(conf, obj['cnf'])

    # Handle rules
    types = {'bitstrings': Bitstring, 'enums': Enum, 'ranges': Range,
             'trailers': Trailer, 'customs': Custom}
    for name, type_ in types.items():
        if name in obj:
            for rule in obj[name]:
                type_(conf, rule)


def handle_options(obj):
    pass


def parse_file(filename, only_text=None):
    """Parse a configuration file."""
    if only_text is not None:
        obj = yaml.safe_load(only_text)
    else:
        with open(filename, 'r') as f:
            obj = yaml.safe_load(f)

    # Deal with options
    if 'Options' in obj:
        handle_options(obj['Options'])

    # Deal with struct rules
    if 'Structs' in obj:
        for struct in obj['Structs']:
            handle_struct(struct)

