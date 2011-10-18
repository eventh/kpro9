"""
Module for testing the config module.
"""
import sys, os
from attest import Tests, assert_hook

import config


# Test that configuration support range rules.
range_rule = Tests()

@range_rule.context
def create_ranges():
    """Create range rules for testing."""
    text = '''
    Structs:
      - name: test
        ranges:
          - member: percent
            min: 10
            max: 30
          - type: int
            max: 15.5
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.configs['test']
    del config.StructConfig.configs['test']

@range_rule.test
def range_rule_member(conf):
    """Test that range rule work for member."""
    assert conf
    rule, = conf.get_rules('percent', None)
    assert rule.max == 30 and rule.min == 10

@range_rule.test
def range_rule_type(conf):
    """Test that range rule work for type."""
    assert conf
    rule, = conf.get_rules('holy hand grenade', 'int')
    assert rule.max == 15.5 and rule.min is None


# Test that configuration support struct id and description.
struct_rule = Tests()

@struct_rule.context
def create_structs():
    """Create structs with id and description."""
    text = '''
    Structs:
      - name: one
        id: 9
        description: a struct
      - name: two
        id: 11
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('one'), config.StructConfig.find('two')
    del config.StructConfig.configs['one']
    del config.StructConfig.configs['two']

@struct_rule.test
def struct_rule_id(one, two):
    """Test config support struct id."""
    assert one and two
    assert one.id == 9 and two.id == 11

@struct_rule.test
def struct_rule_description(one, two):
    """Test config support struct description."""
    assert one and two
    assert one.description == 'a struct' and two.description is None

# Test that configuration support enums
enum = Tests()

@enum.context
def create_enum():
    """Create struct config with enum rules."""
    text = '''
    Structs:
        - name: enum
          id: 10
          description: Enum config test
          enums:
            - member: weekday
              values: {1: MONDAY, 2: TUESDAY, 3: WEDNESDAY, 4: THURSDAY, 5: FRIDAY, 6: SATURDAY, 7: SUNDAY}
            - type: int
              values: [Zero, One, Two, Three, Four, Five]
              strict: True # Disable warning if not a valid value
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('enum')
    del config.StructConfig.configs['enum']

@enum.test
def enum_rule(conf):
    """Test that config support rules for enums."""
    member, type = conf.get_rules('weekday', 'int')
    assert member and type
    assert len(member.values) == 7
    assert member.values[3] == 'WEDNESDAY'
    assert member.strict == True
    assert len(type.values) == 6
    assert type.values[0] == 'Zero'
    assert type.strict == True

# Test that configuration support bit strings
bitstring = Tests()

@bitstring.context
def create_bitstring():
    """Create struct config with bitstring rules."""
    text = '''
    Structs:
      - name: bitstring
        bitstrings:
          - member: flags
            1: Test
            2: [Flag, A, B]
          - type: short
            1-3: [Short, A, B, C, D, E, F, G, H]
            4: [Nih]
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('bitstring')
    del config.StructConfig.configs['bitstring']

@bitstring.test
def bitstring_rule(conf):
    """Test that config support rules for bitstrings."""
    member, type = conf.get_rules('flags', 'short')
    assert member and type
    assert len(member.bits[0]) == 4
    assert member.bits[1][2] == 'Flag'
    assert member.bits[1][3] == {0: 'A', 1: 'B'}
    assert member.bits[0][0] == 1 and member.bits[0][1] == 1
    assert len(type.bits[0][3]) == 8
    assert type.bits[1][2] == 'Nih'
    assert type.bits[1][3] == {0: 'No', 1: 'Yes'}
    assert type.bits[0][0] == 1 and type.bits[0][1] == 3


# Test that configuration support custom fields mapping
fields = Tests()

@fields.context
def create_fields():
    """Create struct config with fields rules."""
    text = '''
    Structs:
      - name: test
        customs:
          - type: time_t
            field: relative_time
          - member: abs
            field: absolute_time
          - type: BOOL
            field: bool
            size: 4
            abbr: bool
            name: A BOOL
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('test')
    del config.StructConfig.configs['test']

@fields.test
def fields_rule(conf):
    """Test that config support rules for custom fields."""
    one, = conf.get_rules('abs', 'short')
    assert one.field == 'absolute_time'
    assert one.size is None and one.abbr is None
    two, = conf.get_rules(None, 'BOOL')
    assert two.field == 'bool' and two.size == 4
    assert two.abbr == 'bool' and two.name == 'A BOOL'
    three, = conf.get_rules(None, 'time_t')
    assert three.field == 'relative_time'
    assert three.size is None and three.abbr is None


# Test that configuration support trailers
trailers = Tests()

@trailers.context
def create_trailers():
    """Create struct config with trailer rules."""
    text = '''
    Structs:
      - name: test
        trailers:
          - name: ber
            count: 3
            size: 8
          - name: ber
            member: asn1_count
            size: 12
          - name: ber
            count: 1
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('test')
    del config.StructConfig.configs['test']

@trailers.test
def trailers_rule(conf):
    """Test that config support rules for trailers."""
    rules = conf.get_rules('asn1_count', None)
    assert len(rules) == 0
    one, two, three = conf.trailers
    assert one.name == 'ber' and three.name == 'ber'
    assert one.count == 3 and two.count is None and three.count == 1
    assert two.member == 'asn1_count' and one.member is None
    assert one.size == 8 and two.size == 12 and three.size is None

