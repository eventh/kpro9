"""
A module for configuration of our utility.

Should parse config files and create which the parser can use.
"""
import sys
import yaml


# Mapping of c type and their wireshark field type.
DEFAULT_C_TYPE_MAP = {
        'bool': 'bool',
        'char': 'string',
        'signed char': 'string',
        'unsigned char': 'string',
        'short': "int16",
        'short int': "int16",
        'signed short int': "int16",
        'unsigned short int': "uint16",
        "int": "int32",
        'signed int': "int32",
        'unsigned int': "uint32",
        'long': "int64",
        'long int': "int64",
        'signed long int': "int64",
        'unsigned long int': "uint64",
        'long long': "int64",
        'long long int': "int64",
        'signed long long int': "int64",
        'unsigned long long int': "uint64",
        'float': 'float',
        'double': 'double',
        'long double': 'todo',
        'pointer': 'int32',
}


# Mapping of c type and their default size in bytes.
DEFAULT_C_SIZE_MAP = {
        'bool': 1,
        'char': 1,
        'signed char': 1,
        'unsigned char': 1,
        'short': 2,
        'short int': 2,
        'signed short int': 2,
        'unsigned short int': 2,
        'int': 4,
        'signed int': 4,
        'unsigned int': 4,
        'long': 8,
        'long int': 8,
        'signed long int': 8,
        'unsigned long int': 8,
        'long long': 8,
        'long long int': 8,
        'signed long long int': 8,
        'unsigned long long int': 8,
        'float': 4,
        'double': 8,
        'long double': 16,
        'pointer': 4,
}

# List of valid C types
VALID_C_TYPES = DEFAULT_C_SIZE_MAP.keys()


class ConfigError(Exception):
    """Exception raised by invalid configuration."""
    pass


class StructConfig:
    """Holds configuration for a specific struct."""
    configs = {}

    def __init__(self, name):
        StructConfig.configs[name] = self

        self.name = name
        self.members = {}
        self.types = {}

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


class RangeRule:
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


def parse_file(filename):
    """Parse a configuration file."""
    with open(filename, 'r') as f:
        obj = yaml.safe_load(f)

    # Deal with range rules
    for rule in obj['RangeRules']:
        RangeRule(rule)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parse_file(sys.argv[1])
    else:
        parse_file('etc/example.yml')
    print(StructConfig.configs)


