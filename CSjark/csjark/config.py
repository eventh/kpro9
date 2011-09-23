"""
A module for configuration of our utility.

Should parse config files and create which the parser can use.
"""
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


class Config:
    """Holds global configuration."""
    singleton = None
    files = {}
    structs = {}
    size_map = DEFAULT_C_SIZE_MAP.copy()

    def __init__(self):
        if Config.singleton is not None:
            raise Exception('Cant have several global config objects.')
        Config.singleton = self

    def get_size_of(self, ctype):
        return self.size_map[ctype]

class FileConfig:
    """Holds configuration for a specific source file."""

    def __init__(self, filename):
        Config.files[filename] = self
        self.filename = filename
        self.rules = []
        self.size_map = {}

    def get_size_of(self, ctype):
        if ctype in self.size_map:
            return self.size_map[ctype]
        else:
            return Config.size_map[ctype]

class StructConfig:
    """Holds configuration for a specific struct."""

    def __init__(self, name):
        Config.structs[name] = self
        self.name = name
        self.rules = []
        self.size_map = {}

    def get_size_of(self, ctype):
        if ctype in self.size_map:
            return self.size_map[ctype]
        else:
            return Config.size_map[ctype]


class RangeRule:
    def __init__(self, obj):
        # Member represents a struct member whom should be validated
        self.member = obj['member']

        # Min and max represents the endpoints of the valid range
        self.min = self.max = None
        if 'min' in obj:
            self.min = float(obj['min'])
        if 'max' in obj:
            self.max = float(obj['max'])


def _handle_file(obj, rule):
    if 'file' in obj:
        name = obj['file']
        if name not in Config.files.keys():
            FileConfig(name)
        config = Config.files[name]
        config.rules.append(rule)

def _handle_struct(obj, rule):
    if 'struct' in obj:
        name = obj['struct']
        if name not in Config.structs.keys():
            StructConfig(name)
        config = Config.structs[name]
        config.rules.append(rule)


def parse(filename):
    """Parse a configuration file."""
    with open(filename, 'r') as f:
        obj = yaml.safe_load(f)
    #print(obj)

    # Deal with range rules
    for rule_obj in obj['RangeRule']:
        rule = RangeRule(rule_obj)
        _handle_file(rule_obj, rule)
        _handle_struct(rule_obj, rule)

    print("Config file '%s' parsed" % filename)
    print(Config.structs)


if __name__ == '__main__':
    parse('etc/example.yml')

