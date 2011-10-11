"""
A module for configuration of our utility.

Should parse config files and create data structures which the parser can
use when translating C struct definitions to Wireshark protocols and fields.
"""
from operator import itemgetter
import yaml


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
        self.members = {}
        self.types = {}

    def get_rules(self, member, type):
        rules = self.members.get(member, [])
        rules.extend(self.types.get(type, []))
        return rules

    def add_member_rule(self, member, rule):
        if member not in self.members.keys():
            self.members[member] = []
        self.members[member].append(rule)

    def add_type_rule(self, type, rule):
        if type not in self.types.keys():
            self.types[type] = []
        self.types[type].append(rule)

    @classmethod
    def find(cls, name):
        if name not in cls.configs.keys():
            return cls(name)
        else:
            return cls.configs[name]


class BaseRule:
    """A base class for rules refering to protocol fields."""

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
            raise ConfigError('RangeRule needs atleast a min or max value.')


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


class Dissector(BaseRule):
    """Rule for specifying a trailer?."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)
        self.name = str(obj['name'])
        self.size = None
        if 'size' in obj:
            self.size = int(obj['size'])
        if not self.name:
            raise ConfigError('Invalid dissector rule for %s' % conf.name)


def handle_struct(obj):
    """Handle rules and configuration for a struct."""
    conf = StructConfig.find(obj['name'])

    # Structs optional id
    if 'id' in obj:
        conf.id = int(obj['id'])

    # Structs optional description
    if 'description' in obj:
        conf.description = obj['description']

    # Handle bitstrings
    if 'bitstrings' in obj:
        for rule in obj['bitstrings']:
            Bitstring(conf, rule)

    # Handle enums
    if 'enums' in obj:
        for rule in obj['enums']:
            Enum(conf, rule)

    # Handle ranges
    if 'ranges' in obj:
        for rule in obj['ranges']:
            Range(conf, rule)

    # Handle specific dissectors
    if 'dissectors' in obj:
        for rule in obj['dissectors']:
            Dissector(conf, rule)


def handle_options(obj):
    return


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

