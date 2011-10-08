"""
A module for configuration of our utility.

Should parse config files and create data structures which the parser can
use when translating C struct definitions to Wireshark protocols and fields.
"""
import yaml
from operator import itemgetter


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


class BaseFieldRule:
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


class RangeRule(BaseFieldRule):
    """Rule for specifying a valid range for a struct member or type."""

    def __init__(self, obj):
        self.struct = obj['struct']
        conf = StructConfig.find(self.struct)
        super().__init__(conf, obj)

        # Min and max represents the endpoints of the valid range
        self.min = self.max = None
        if 'min' in obj:
            self.min = float(obj['min'])
        if 'max' in obj:
            self.max = float(obj['max'])
        if self.min is None and self.max is None:
            raise ConfigError('RangeRule needs atleast a min or max value.')


class Bitstring(BaseFieldRule):
    """Rule for representing bit strings in structs."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)

        # Find all bitstring defintions
        self.values = []
        for key, value in obj.items():
            try:
                int(key)
            except ValueError:
                if '-' not in key:
                    raise ConfigError('Invalid bitstring key: %s' % key)
                start, end = [int(i) for i in key.split('-')]
                offset = end - start + 1
            else:
                start, offset = key, 1
            if isinstance(value, str):
                value = ['%s: No' % value, '%s: Yes' % value]
            self.values.append([start, offset, value])

        self.values.sort(key=itemgetter(0))
        if not self.values:
            raise ConfigError('Invalid bitstring rule for %s' % conf.name)


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

    # Handle ranges
    if 'ranges' in obj:
        pass # Move RangeRules handling to here


def parse_file(filename, only_text=None):
    """Parse a configuration file."""
    if only_text is not None:
        obj = yaml.safe_load(only_text)
    else:
        with open(filename, 'r') as f:
            obj = yaml.safe_load(f)

    # Deal with struct rules
    if 'Structs' in obj:
        for struct in obj['Structs']:
            handle_struct(struct)

    # Deal with range rules
    if 'RangeRules' in obj:
        for rule in obj['RangeRules']:
            RangeRule(rule)

