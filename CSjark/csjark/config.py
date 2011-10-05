"""
A module for configuration of our utility.

Should parse config files and create data structures which the parser can
use when translating C struct definitions to Wireshark protocols and fields.
"""
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


class StructRule:
    """Rule for specifying attributes on structs."""

    def __init__(self, obj):
        self.name = obj['name']
        conf = StructConfig.find(self.name)

        # Structs ID
        self.id = obj['id']
        conf.id = self.id

        # Structs optional description
        self.description = obj['description']
        conf.description = self.description


class RangeRule:
    """Rule for specifying a valid range for a struct member or type."""

    def __init__(self, obj):
        self.struct = obj['struct']
        conf = StructConfig.find(self.struct)

        # A range rule refers either to a type or a member
        self.member = self.type = None
        if 'member' in obj:
            self.member = obj['member']
            conf.add_member_rule(self.member, self)
        elif 'type' in obj:
            self.type = obj['type']
            conf.add_type_rule(self.type, self)
        else:
            raise ConfigError('RangeRule needs either a type or member.')

        # Min and max represents the endpoints of the valid range
        self.min = self.max = None
        if 'min' in obj:
            self.min = float(obj['min'])
        if 'max' in obj:
            self.max = float(obj['max'])
        if self.min is None and self.max is None:
            raise ConfigError('RangeRule needs atleast a min or max value.')


def parse_file(filename, only_text=None):
    """Parse a configuration file."""
    if only_text is not None:
        obj = yaml.safe_load(only_text)
    else:
        with open(filename, 'r') as f:
            obj = yaml.safe_load(f)
    print(obj)

    # Deal with struct rules
    if 'Structs' in obj:
        for rule in obj['Structs']:
            StructRule(rule)

    # Deal with range rules
    if 'RangeRules' in obj:
        for rule in obj['RangeRules']:
            RangeRule(rule)

