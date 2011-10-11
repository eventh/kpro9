"""
Module for testing the config module.
"""
import sys, os
from attest import Tests, assert_hook

try:
    import config
except ImportError:
    # If cparser is not installed, look in parent folder
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))
    import config


# Test that configuration support range rules.
range_rule = Tests()

@range_rule.context
def create_ranges():
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
    assert conf
    rule, = conf.get_rules('percent', None)
    assert rule.max == 30 and rule.min == 10

@range_rule.test
def range_rule_type(conf):
    assert conf
    rule, = conf.get_rules('holy hand grenade', 'int')
    assert rule.max == 15.5 and rule.min is None


# Test that configuration support struct id and description.
struct_rule = Tests()

@struct_rule.context
def create_structs():
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
    assert one and two
    assert one.id == 9 and two.id == 11

@struct_rule.test
def struct_rule_description(one, two):
    assert one and two
    assert one.description == 'a struct' and two.description is None


# Test that configuration support bit strings
bitstring = Tests()

@bitstring.context
def create_bitstring():
    text = '''
    Structs:
      - name: bitstring
        bitstrings:
          - member: flags
            0: Test
            1: [Flag, A, B]
          - type: short
            0-2: [Short, A, B, C, D, E, F, G, H]
            3: [Nih]
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('bitstring')
    del config.StructConfig.configs['bitstring']

@bitstring.test
def bitstring_rule(conf):
    member, type = conf.get_rules('flags', 'short')
    assert member and type
    assert len(member.bits[0]) == 4
    assert member.bits[1][2] == 'Flag'
    assert member.bits[1][3] == {0: 'A', 1: 'B'}
    assert len(type.bits[0][3]) == 8
    assert type.bits[1][2] == 'Nih'
    assert type.bits[1][3] == {0: 'No', 1: 'Yes'}


if __name__ == '__main__':
    all_tests = Tests([range_rule, struct_rule, bitstring])
    all_tests.run()

