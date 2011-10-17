"""
A module for black box testing of our program.

Should have tests for the major requirements.
"""
"""
Module for testing the dissector module.

Tests the output of generating dissectors.
"""
import sys, os
from attest import Tests, assert_hook, contexts

import dissector
from config import StructConfig


def compare_lua(code, template, write_to_file=''):
    """Test that generated lua code equals what is expected."""
    if write_to_file:
        with open(write_to_file, 'a') as f:
            f.write('%s\n' % code.replace('\t',''))
    def simplify(text):
        return ''.join(text.strip().split())
    return simplify(code) == simplify(template)


blackBox = Tests()

#testing header files with several different types of input like arrays, enums, structs within structs etc

@blackBox.test
def Holy_hand_grenade():
    #todo, use compare_lua to compare correct LUA code to the generated code from csjark.
    pass



