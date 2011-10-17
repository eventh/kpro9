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

import dissector,csjark,config,cparser


def compare_lua(code, template, write_to_file=''):
    """Test that generated lua code equals what is expected."""
    if write_to_file:
        with open(write_to_file, 'a') as f:
            f.write('%s\n' % code.replace('\t',''))
    def simplify(text):
        return ''.join(text.strip().split())

    return simplify(code) == simplify(template)

def test_dissector(filename):
    """Create a Wireshark dissector from 'filename'."""
    ast = cparser.parse_file(filename, use_cpp=csjark.Cli.use_cpp)

    protocols = cparser.find_structs(ast)

    result = ''

    # Generate and write lua dissectors
    for proto in protocols:
        code = proto.create()
        result += code

    return result


blackBox = Tests()

def run_csjark(args):
        """Run the CSjark program."""
        headers, configs = csjark.Cli.parse_args(args)

        # Parse config files
        for filename in configs:
            config.parse_file(filename)

    # Create dissectors
        dissector = ''
        for filename in headers:
            dissector += test_dissector(filename)
        return dissector


#testing header files with several different types of input like arrays, enums, structs within structs etc

@blackBox.test
def enum_test():
    #todo, use compare_lua to compare correct LUA code to the generated code from csjark.
    dissector = run_csjark(['headers\cenum_test.h', 'etc\cenum_test.yml'])
    assert compare_lua(dissector,'''-- Dissector for struct: cenum_test: C Enum test
        local proto_cenum_test = Proto("cenum_test", "C Enum test")
        local luastructs_dt = DissectorTable.get("luastructs.message")

        -- ProtoField defintions for struct: cenum_test
        local f = proto_cenum_test.fields
        f.id = ProtoField.int32("cenum_test.id", "id")
        f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"})

        -- Dissector function for struct: cenum_test
        function proto_cenum_test.diasdaddaddssector(buffer, pinfo, tree)
                local subtree = tree:add(proto_cenum_test, buffer())
                pinfo.cols.info:append(" (" .. proto_cenum_test.description .. ")")

                subtree:add(f.id, buffer(0, 4))
                local mnd = subtree:add(f.mnd, buffer(4, 4))
                local test = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"}
                if (test[buffer(4, 4):uint()] == nil) then
                        mnd:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20)")
                end
        end

        luastructs_dt:add(11, proto_cenum_test)
        ''')




if __name__ == '__main__':
    blackBox.run()
