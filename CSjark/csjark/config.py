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

    def get_rules(self, member, type, sorted=False):
        rules = self.members.get(member, [])
        rules.extend(self.types.get(type, []))

        if not sorted:
            return rules

        # Sort the rules
        types = (Dissector, Bitstring, Enum, Range, Field)
        values = ([], [], [], [], [])
        for rule in rules:
            for i, type_ in enumerate(types):
                if isinstance(rule, type_):
                    values[i].append(rule)
        return values

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


class Field(BaseRule):
    """Rule for specifying a custom field handling."""

    def __init__(self, conf, obj):
        super().__init__(conf, obj)
        self.field = str(obj['field'])
        self.size = obj.get('size', None)
        self.abbr = obj.get('abbr', None)
        self.name = obj.get('name', None)
        self.base = obj.get('base', None)
        self.values = obj.get('values', None)
        self.mask = obj.get('mask', None)
        self.desc = obj.get('desc', None)
        if not self.field:
            raise ConfigError('No field for Field rule for %s' % conf.name)

    def create(self, cls, name, size):
        if self.size is not None:
            size = self.size
        field = cls(name, self.field, size)
        field.abbr = self.abbr
        field.base = self.base
        if self.values:
            field.values = field._dict_to_table(self.values)
        field.mask = self.mask
        field.desc = self.desc
        return field


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

    # Handle rules
    types = {'bitstrings': Bitstring, 'enums': Enum, 'ranges': Range,
             'dissectors': Dissector, 'fields': Field}
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

