"""
A module for configuration of our utility.

Should parse config files and create which the parser can use.
"""
import yaml
from RangeRule import RangeRule

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
        self.size_map = {}

    def get_size_of(self, ctype):
        if ctype in self.size_map:
            return self.size_map[ctype]
        else:
            return Config.size_map[ctype]


def parse(filename):
    """Parse a configuration file."""
    stream = open(filename, 'r')
    config = yaml.load(stream)
    rules = []
    
    print(config.keys())
    
    for i in range(len(config['RangeRule'])):
        b = RangeRule(0,0,0)
        a = RangeRule(config['RangeRule'][i]['file'], config['RangeRule'][i]['struct'], config['RangeRule'][i]['member'])
        a.setType(config['RangeRule'][i]['type'])
        a.setMinvalue(config['RangeRule'][i]['minvalue'])
        a.setMaxvalue(config['RangeRule'][i]['maxvalue'])
        rules.append(a)
     
    print(len(config['RangeRule']), "config rules parsed")

parse('configuration/example.yml')