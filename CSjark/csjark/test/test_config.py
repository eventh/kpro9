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
def create_rules():
    text = '''
    RangeRules:
      - struct: test
        member: percent
        min: 10
        max: 30
      - struct: test
        type: int
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


if __name__ == '__main__':
    all_tests = Tests([range_rule])
    all_tests.run()

