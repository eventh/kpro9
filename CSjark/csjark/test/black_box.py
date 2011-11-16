"""
A module for black box testing of our program.

Should have tests for the major requirements.
"""
import sys, os
from attest import Tests, assert_hook, contexts

import csjark
import cparser
import config
import dissector

from .test_dissector import compare_lua


def create_protocols(headers, yml, args=None, cleanup=True):
    """Create protocols for black-box-testing."""
    # Store default options to be able to restore them later
    config.Options.platforms = set()
    o = config.Options
    defaults = (o.verbose, o.debug, o.strict, o.use_cpp,
                o.output_dir, o.output_file, o.platforms, o.delegator)

    # Parse command line arguments
    if args is None:
        args = []
    cli_args = ['-f'] + headers + ['-c', yml] + args
    headers, configs = csjark.parse_args(cli_args)

    # Parse config files
    for filename in configs:
        config.parse_file(filename)
    config.Options.prepare_for_parsing()

    # Create protocols
    csjark.parse_headers(headers)

    # Sort the protocols on name
    structs = {}
    for key, proto in cparser.StructVisitor.all_protocols.items():
        structs[proto.name] = proto.generate()

    if cleanup:
        perform_cleanup(defaults)
        return structs
    else:
        return structs, defaults

def perform_cleanup(defaults):
    """Clean up after running create_protocols."""
    dissector.Protocol.protocols = {}
    config.Options.platforms = set()
    cparser.StructVisitor.all_protocols = {}
    config.Options.configs = {}
    (config.Options.verbose, config.Options.debug,
            config.Options.strict, config.Options.use_cpp,
            config.Options.output_dir, config.Options.output_file,
            config.Options.platforms, config.Options.delegator) = defaults


# End-to-end tests for sprint 2 features
sprint2 = Tests()

@sprint2.context
def create_sprint2(structs={}):
    """Create protocols for all structs in sprint2.h"""
    if not structs:
        header = os.path.join(os.path.dirname(__file__), 'sprint2.h')
        yml = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
        structs.update(create_protocols([header], yml))
    yield structs


@sprint2.test
def cenums(structs):
    """End-to-end test headers with C enums in them."""
    assert 'cenum_test' in structs
    assert structs['cenum_test']
    assert compare_lua(structs['cenum_test'], '''
    -- Dissector for cenum_test: C Enum test
    local proto_cenum_test = Proto("cenum_test", "C Enum test")
    -- ProtoField defintions for: cenum_test
    local f = proto_cenum_test.fields
    f.id = ProtoField.int32("cenum_test.id", "id")
    local mnd_valuestring = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"}
    f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, mnd_valuestring)
    -- Dissector function for: cenum_test
    function proto_cenum_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_cenum_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": cenum_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(C Enum test)")
    end
    subtree:add(f.id, buffer(0, 4))
    local mnd_node = subtree:add(f.mnd, buffer(4, 4))
    local mnd_value = buffer(4, 4):uint()
    if mnd_valuestring[mnd_value] == nil then
    mnd_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20]")
    end
    end
    delegator_register_proto(proto_cenum_test, "cenum_test", 11, {[0]=8})
    ''')


@sprint2.test
def arrays(structs):
    """End-to-end test headers with arrays in them."""
    assert 'array_test' in structs
    assert structs['array_test']
    assert compare_lua(structs['array_test'], '''
    -- Dissector for array_test: Multidimensional array
    local proto_array_test = Proto("array_test", "Multidimensional array")
    -- ProtoField defintions for: array_test
    local f = proto_array_test.fields
    f.chararr1 = ProtoField.string("array_test.chararr1", "chararr1")
    f.intarr2 = ProtoField.bytes("array_test.intarr2", "intarr2")
    f.intarr2_0 = ProtoField.bytes("array_test.intarr2.0", "intarr2[0]")
    f.intarr2_0_0 = ProtoField.int32("array_test.intarr2.0.0", "intarr2[0][0]")
    f.intarr2_0_1 = ProtoField.int32("array_test.intarr2.0.1", "intarr2[0][1]")
    f.intarr2_0_2 = ProtoField.int32("array_test.intarr2.0.2", "intarr2[0][2]")
    f.intarr2_0_3 = ProtoField.int32("array_test.intarr2.0.3", "intarr2[0][3]")
    f.intarr2_1 = ProtoField.bytes("array_test.intarr2.1", "intarr2[1]")
    f.intarr2_1_0 = ProtoField.int32("array_test.intarr2.1.0", "intarr2[1][0]")
    f.intarr2_1_1 = ProtoField.int32("array_test.intarr2.1.1", "intarr2[1][1]")
    f.intarr2_1_2 = ProtoField.int32("array_test.intarr2.1.2", "intarr2[1][2]")
    f.intarr2_1_3 = ProtoField.int32("array_test.intarr2.1.3", "intarr2[1][3]")
    f.intarr2_2 = ProtoField.bytes("array_test.intarr2.2", "intarr2[2]")
    f.intarr2_2_0 = ProtoField.int32("array_test.intarr2.2.0", "intarr2[2][0]")
    f.intarr2_2_1 = ProtoField.int32("array_test.intarr2.2.1", "intarr2[2][1]")
    f.intarr2_2_2 = ProtoField.int32("array_test.intarr2.2.2", "intarr2[2][2]")
    f.intarr2_2_3 = ProtoField.int32("array_test.intarr2.2.3", "intarr2[2][3]")
    f.intarr2_3 = ProtoField.bytes("array_test.intarr2.3", "intarr2[3]")
    f.intarr2_3_0 = ProtoField.int32("array_test.intarr2.3.0", "intarr2[3][0]")
    f.intarr2_3_1 = ProtoField.int32("array_test.intarr2.3.1", "intarr2[3][1]")
    f.intarr2_3_2 = ProtoField.int32("array_test.intarr2.3.2", "intarr2[3][2]")
    f.intarr2_3_3 = ProtoField.int32("array_test.intarr2.3.3", "intarr2[3][3]")
    f.chararr3 = ProtoField.string("array_test.chararr3", "chararr3")
    f.chararr3_0 = ProtoField.string("array_test.chararr3.0", "chararr3[0]")
    f.chararr3_1 = ProtoField.string("array_test.chararr3.1", "chararr3[1]")
    f.floatarr4 = ProtoField.bytes("array_test.floatarr4", "floatarr4")
    f.floatarr4_0 = ProtoField.bytes("array_test.floatarr4.0", "floatarr4[0]")
    f.floatarr4_0_0 = ProtoField.float("array_test.floatarr4.0.0", "floatarr4[0][0]")
    f.floatarr4_0_1 = ProtoField.float("array_test.floatarr4.0.1", "floatarr4[0][1]")
    f.floatarr4_0_2 = ProtoField.float("array_test.floatarr4.0.2", "floatarr4[0][2]")
    f.floatarr4_1 = ProtoField.bytes("array_test.floatarr4.1", "floatarr4[1]")
    f.floatarr4_1_0 = ProtoField.float("array_test.floatarr4.1.0", "floatarr4[1][0]")
    f.floatarr4_1_1 = ProtoField.float("array_test.floatarr4.1.1", "floatarr4[1][1]")
    f.floatarr4_1_2 = ProtoField.float("array_test.floatarr4.1.2", "floatarr4[1][2]")
    -- Dissector function for: array_test
    function proto_array_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_array_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": array_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Multidimensional array)")
    end
    subtree:add(f.chararr1, buffer(0, 16))
    local array = subtree:add(f.intarr2, buffer(16, 64))
    array:set_text("intarr2 (16 x int32)")
    local subarray = array:add(f.intarr2_0, buffer(16, 16))
    subarray:set_text("intarr2[0] (4 x int32)")
    subarray:add(f.intarr2_0_0, buffer(16, 4))
    subarray:add(f.intarr2_0_1, buffer(20, 4))
    subarray:add(f.intarr2_0_2, buffer(24, 4))
    subarray:add(f.intarr2_0_3, buffer(28, 4))
    local subarray = array:add(f.intarr2_1, buffer(32, 16))
    subarray:set_text("intarr2[1] (4 x int32)")
    subarray:add(f.intarr2_1_0, buffer(32, 4))
    subarray:add(f.intarr2_1_1, buffer(36, 4))
    subarray:add(f.intarr2_1_2, buffer(40, 4))
    subarray:add(f.intarr2_1_3, buffer(44, 4))
    local subarray = array:add(f.intarr2_2, buffer(48, 16))
    subarray:set_text("intarr2[2] (4 x int32)")
    subarray:add(f.intarr2_2_0, buffer(48, 4))
    subarray:add(f.intarr2_2_1, buffer(52, 4))
    subarray:add(f.intarr2_2_2, buffer(56, 4))
    subarray:add(f.intarr2_2_3, buffer(60, 4))
    local subarray = array:add(f.intarr2_3, buffer(64, 16))
    subarray:set_text("intarr2[3] (4 x int32)")
    subarray:add(f.intarr2_3_0, buffer(64, 4))
    subarray:add(f.intarr2_3_1, buffer(68, 4))
    subarray:add(f.intarr2_3_2, buffer(72, 4))
    subarray:add(f.intarr2_3_3, buffer(76, 4))
    local array = subtree:add(f.chararr3, buffer(80, 6))
    array:add(f.chararr3_0, buffer(80, 3))
    array:add(f.chararr3_1, buffer(83, 3))
    local array = subtree:add(f.floatarr4, buffer(86, 24))
    array:set_text("floatarr4 (6 x float)")
    local subarray = array:add(f.floatarr4_0, buffer(86, 12))
    subarray:set_text("floatarr4[0] (3 x float)")
    subarray:add(f.floatarr4_0_0, buffer(86, 4))
    subarray:add(f.floatarr4_0_1, buffer(90, 4))
    subarray:add(f.floatarr4_0_2, buffer(94, 4))
    local subarray = array:add(f.floatarr4_1, buffer(98, 12))
    subarray:set_text("floatarr4[1] (3 x float)")
    subarray:add(f.floatarr4_1_0, buffer(98, 4))
    subarray:add(f.floatarr4_1_1, buffer(102, 4))
    subarray:add(f.floatarr4_1_2, buffer(106, 4))
    end
    delegator_register_proto(proto_array_test, "array_test", 16, {[0]=110})
    ''')


@sprint2.test
def bitstrings(structs):
    """End-to-end test headers with bitstrings in them."""
    assert 'bitstring_test' in structs
    assert structs['bitstring_test']
    assert compare_lua(structs['bitstring_test'], '''
    -- Dissector for bitstring_test: Bit string test
    local proto_bitstring_test = Proto("bitstring_test", "Bit string test")
    -- ProtoField defintions for: bitstring_test
    local f = proto_bitstring_test.fields
    f.id = ProtoField.int32("bitstring_test.id", "id")
    f.flags = ProtoField.uint32("bitstring_test.flags", "flags (bitstring)", base.HEX)
    f.flags_inuse = ProtoField.uint32("bitstring_test.flags.In_use", "In use", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.flags_endian = ProtoField.uint32("bitstring_test.flags.Endian", "Endian", nil, {[0]="Big", [1]="Little"}, 0x2)
    f.flags_platform = ProtoField.uint32("bitstring_test.flags.Platform", "Platform", nil, {[0]="Win", [1]="Linux", [2]="Mac", [3]="Solaris"}, 0xc)
    f.flags_test = ProtoField.uint32("bitstring_test.flags.Test", "Test", nil, {[0]="No", [1]="Yes"}, 0x10)
    f.color1 = ProtoField.uint16("bitstring_test.color1", "color1 (bitstring)", base.HEX)
    f.color1_red = ProtoField.uint16("bitstring_test.color1.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.color1_blue = ProtoField.uint16("bitstring_test.color1.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.color1_green = ProtoField.uint16("bitstring_test.color1.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
    f.color2 = ProtoField.uint16("bitstring_test.color2", "color2 (bitstring)", base.HEX)
    f.color2_red = ProtoField.uint16("bitstring_test.color2.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.color2_blue = ProtoField.uint16("bitstring_test.color2.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.color2_green = ProtoField.uint16("bitstring_test.color2.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
    -- Dissector function for: bitstring_test
    function proto_bitstring_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_bitstring_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": bitstring_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Bit string test)")
    end
    subtree:add(f.id, buffer(0, 4))
    local bittree = subtree:add(f.flags, buffer(4, 4))
    bittree:add(f.flags_inuse, buffer(4, 4))
    bittree:add(f.flags_endian, buffer(4, 4))
    bittree:add(f.flags_platform, buffer(4, 4))
    bittree:add(f.flags_test, buffer(4, 4))
    local bittree = subtree:add(f.color1, buffer(8, 2))
    bittree:add(f.color1_red, buffer(8, 2))
    bittree:add(f.color1_blue, buffer(8, 2))
    bittree:add(f.color1_green, buffer(8, 2))
    local bittree = subtree:add(f.color2, buffer(10, 2))
    bittree:add(f.color2_red, buffer(10, 2))
    bittree:add(f.color2_blue, buffer(10, 2))
    bittree:add(f.color2_green, buffer(10, 2))
    end
    delegator_register_proto(proto_bitstring_test, "bitstring_test", 13, {[0]=12})
    ''')


@sprint2.test
def custom(structs):
    """End-to-end test headers with custom field rules."""
    assert 'custom_lua' in structs
    assert structs['custom_lua']
    assert compare_lua(structs['custom_lua'], '''
    -- Dissector for custom_lua: struct custom_lua
    local proto_custom_lua = Proto("custom_lua", "struct custom_lua")
    -- ProtoField defintions for: custom_lua
    local f = proto_custom_lua.fields
    f.normal = ProtoField.int16("custom_lua.normal", "normal")
    f.special = ProtoField.int64("custom_lua.special", "special")
    f.abs = ProtoField.absolute_time("custom_lua.abs", "abs")
    f.rel = ProtoField.relative_time("custom_lua.rel", "rel")
    f.abool = ProtoField.bool("custom_lua.bool", "A BOOL")
    f.something = ProtoField.uint32("custom_lua.all.all", "Something", base.HEX, {[0]="Monday", [1]="Tuesday"}, nil, "This is something dark side!")
    local truth_valuestring = {[0]="TRUE", [1]="FALSE"}
    f.truth = ProtoField.uint32("custom_lua.truth", "truth", nil, truth_valuestring)
    f.five = ProtoField.bytes("custom_lua.five", "five")
    f.five_0 = ProtoField.int32("custom_lua.five.0", "five[0]")
    f.five_1 = ProtoField.int32("custom_lua.five.1", "five[1]")
    f.five_2 = ProtoField.int32("custom_lua.five.2", "five[2]")
    f.five_3 = ProtoField.int32("custom_lua.five.3", "five[3]")
    f.five_4 = ProtoField.int32("custom_lua.five.4", "five[4]")
    f.pointer = ProtoField.int32("custom_lua.pointer", "pointer")
    f.str = ProtoField.string("custom_lua.str", "str")
    f.str_0 = ProtoField.string("custom_lua.str.0", "str[0]")
    f.str_0_0 = ProtoField.string("custom_lua.str.0.0", "str[0][0]")
    f.str_0_1 = ProtoField.string("custom_lua.str.0.1", "str[0][1]")
    f.str_0_2 = ProtoField.string("custom_lua.str.0.2", "str[0][2]")
    f.str_1 = ProtoField.string("custom_lua.str.1", "str[1]")
    f.str_1_0 = ProtoField.string("custom_lua.str.1.0", "str[1][0]")
    f.str_1_1 = ProtoField.string("custom_lua.str.1.1", "str[1][1]")
    f.str_1_2 = ProtoField.string("custom_lua.str.1.2", "str[1][2]")
    f.str_2 = ProtoField.string("custom_lua.str.2", "str[2]")
    f.str_2_0 = ProtoField.string("custom_lua.str.2.0", "str[2][0]")
    f.str_2_1 = ProtoField.string("custom_lua.str.2.1", "str[2][1]")
    f.str_2_2 = ProtoField.string("custom_lua.str.2.2", "str[2][2]")
    f.str_3 = ProtoField.string("custom_lua.str.3", "str[3]")
    f.str_3_0 = ProtoField.string("custom_lua.str.3.0", "str[3][0]")
    f.str_3_1 = ProtoField.string("custom_lua.str.3.1", "str[3][1]")
    f.str_3_2 = ProtoField.string("custom_lua.str.3.2", "str[3][2]")
    -- Dissector function for: custom_lua
    function proto_custom_lua.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_custom_lua, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": custom_lua")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct custom_lua)")
    end
    subtree:add(f.normal, buffer(0, 2))
    subtree:add(f.special, buffer(8, 8))
    subtree:add(f.abs, buffer(16, 4))
    subtree:add(f.rel, buffer(20, 4))
    subtree:add(f.abool, buffer(24, 4))
    subtree:add(f.something, buffer(28, 4))
    local truth_node = subtree:add(f.truth, buffer(32, 4))
    local truth_value = buffer(32, 4):uint()
    if truth_valuestring[truth_value] == nil then
    truth_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1]")
    end
    local array = subtree:add(f.five, buffer(36, 20))
    array:set_text("five (5 x int32)")
    array:add(f.five_0, buffer(36, 4))
    array:add(f.five_1, buffer(40, 4))
    array:add(f.five_2, buffer(44, 4))
    array:add(f.five_3, buffer(48, 4))
    array:add(f.five_4, buffer(52, 4))
    subtree:add(f.pointer, buffer(56, 4))
    local array = subtree:add(f.str, buffer(60, 24))
    local subarray = array:add(f.str_0, buffer(60, 6))
    subarray:add(f.str_0_0, buffer(60, 2))
    subarray:add(f.str_0_1, buffer(62, 2))
    subarray:add(f.str_0_2, buffer(64, 2))
    local subarray = array:add(f.str_1, buffer(66, 6))
    subarray:add(f.str_1_0, buffer(66, 2))
    subarray:add(f.str_1_1, buffer(68, 2))
    subarray:add(f.str_1_2, buffer(70, 2))
    local subarray = array:add(f.str_2, buffer(72, 6))
    subarray:add(f.str_2_0, buffer(72, 2))
    subarray:add(f.str_2_1, buffer(74, 2))
    subarray:add(f.str_2_2, buffer(76, 2))
    local subarray = array:add(f.str_3, buffer(78, 6))
    subarray:add(f.str_3_0, buffer(78, 2))
    subarray:add(f.str_3_1, buffer(80, 2))
    subarray:add(f.str_3_2, buffer(82, 2))
    end
    delegator_register_proto(proto_custom_lua, "custom_lua", 74, {[0]=88})
''')


@sprint2.test
def enums(structs):
    """End-to-end test headers with enums in them."""
    assert 'enum_test' in structs
    assert structs['enum_test']
    assert compare_lua(structs['enum_test'], '''
    -- Dissector for enum_test: Enum config test
    local proto_enum_test = Proto("enum_test", "Enum config test")
    -- ProtoField defintions for: enum_test
    local f = proto_enum_test.fields
    local id_valuestring = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
    f.id = ProtoField.int32("enum_test.id", "id", nil, id_valuestring)
    f.name = ProtoField.string("enum_test.name", "name")
    local weekday_valuestring = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
    f.weekday = ProtoField.int32("enum_test.weekday", "weekday", nil, weekday_valuestring)
    local number_valuestring = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
    f.number = ProtoField.int32("enum_test.number", "number", nil, number_valuestring)
    -- Dissector function for: enum_test
    function proto_enum_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_enum_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": enum_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Enum config test)")
    end
    local id_node = subtree:add(f.id, buffer(0, 4))
    local id_value = buffer(0, 4):int()
    if id_valuestring[id_value] == nil then
    id_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4, 5]")
    end
    subtree:add(f.name, buffer(4, 10))
    local weekday_node = subtree:add(f.weekday, buffer(16, 4))
    local weekday_value = buffer(16, 4):int()
    if weekday_valuestring[weekday_value] == nil then
    weekday_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4, 5]")
    end
    local number_node = subtree:add(f.number, buffer(20, 4))
    local number_value = buffer(20, 4):int()
    if number_valuestring[number_value] == nil then
    number_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4, 5]")
    end
    end
    delegator_register_proto(proto_enum_test, "enum_test", 10, {[0]=24})
    ''')


@sprint2.test
def ranges(structs):
    """End-to-end test headers with ranges in them."""
    assert 'range_test' in structs
    assert structs['range_test']
    assert compare_lua(structs['range_test'], '''
    -- Dissector for range_test: Range rules test
    local proto_range_test = Proto("range_test", "Range rules test")
    -- ProtoField defintions for: range_test
    local f = proto_range_test.fields
    f.name = ProtoField.string("range_test.name", "name")
    f.age = ProtoField.int32("range_test.age", "age")
    -- Dissector function for: range_test
    function proto_range_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_range_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": range_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Range rules test)")
    end
    subtree:add(f.name, buffer(0, 10))
    local age_node = subtree:add(f.age, buffer(12, 4))
    local age_value = buffer(12, 4):int()
    if age_value < 0.0 then
    age_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
    end
    if age_value > 100.0 then
    age_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 100.0")
    end
    end
    delegator_register_proto(proto_range_test, "range_test", 9, {[0]=16})
    ''')


@sprint2.test
def struct_within_struct(structs):
    """End-to-end test of structs within structs."""
    assert 'struct_within_struct_test' in structs
    assert structs['struct_within_struct_test']
    assert compare_lua(structs['struct_within_struct_test'], '''
    -- Dissector for struct_within_struct_test: Struct in struct test
    local proto_struct_within_struct_test = Proto("struct_within_struct_test", "Struct in struct test")
    -- ProtoField defintions for: struct_within_struct_test
    local f = proto_struct_within_struct_test.fields
    f.prime = ProtoField.int32("struct_within_struct_test.prime", "prime")
    -- Dissector function for: struct_within_struct_test
    function proto_struct_within_struct_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_struct_within_struct_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": struct_within_struct_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Struct in struct test)")
    end
    subtree:add(f.prime, buffer(0, 4))
    pinfo.private.field_name = "astruct"
    Dissector.get("cenum_test"):call(buffer(4, 8):tvb(), pinfo, subtree)
    end
    delegator_register_proto(proto_struct_within_struct_test, "struct_within_struct_test", 12, {[0]=12})
    ''')


@sprint2.test
def trailers(structs):
    """End-to-end test headers with trailers in them."""
    assert 'trailer_test' in structs
    assert structs['trailer_test']
    assert compare_lua(structs['trailer_test'], '''
    -- Dissector for trailer_test: struct trailer_test
    local proto_trailer_test = Proto("trailer_test", "struct trailer_test")
    -- ProtoField defintions for: trailer_test
    local f = proto_trailer_test.fields
    f.tmp = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp_0 = ProtoField.float("trailer_test.tmp.0", "tmp[0]")
    f.tmp_1 = ProtoField.float("trailer_test.tmp.1", "tmp[1]")
    f.tmp_2 = ProtoField.float("trailer_test.tmp.2", "tmp[2]")
    f.tmp_3 = ProtoField.float("trailer_test.tmp.3", "tmp[3]")
    f.tmp_4 = ProtoField.float("trailer_test.tmp.4", "tmp[4]")
    f.asn1_count = ProtoField.int32("trailer_test.asn1_count", "asn1_count")
    -- Dissector function for: trailer_test
    function proto_trailer_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_trailer_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": trailer_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct trailer_test)")
    end
    local array = subtree:add(f.tmp, buffer(0, 20))
    array:set_text("tmp (5 x float)")
    array:add(f.tmp_0, buffer(0, 4))
    array:add(f.tmp_1, buffer(4, 4))
    array:add(f.tmp_2, buffer(8, 4))
    array:add(f.tmp_3, buffer(12, 4))
    array:add(f.tmp_4, buffer(16, 4))
    subtree:add(f.asn1_count, buffer(20, 4))
    -- Trailers handling for struct: trailer_test
    local trail_offset = 24
    local trail_count = buffer(20, 4):int()
    for i = 1, trail_count do
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset, 6):tvb(), pinfo, tree)
    trail_offset = trail_offset + 6
    end
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset, 5):tvb(), pinfo, tree)
    trail_offset = trail_offset + 5
    for i = 1, 2 do
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset, 6):tvb(), pinfo, tree)
    trail_offset = trail_offset + 6
    end
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset):tvb(), pinfo, tree)
    end
    delegator_register_proto(proto_trailer_test, "trailer_test", 66, {[0]=24})
    ''')


# End-to-end tests for sprint 3 features
sprint3 = Tests()

@sprint3.context
def create_sprint3(structs={}):
    """Create protocols for all structs in sprint2.h"""
    if not structs:
        header = os.path.join(os.path.dirname(__file__), 'sprint3.h')
        yml = os.path.join(os.path.dirname(__file__), 'sprint3.yml')
        structs.update(create_protocols([header], yml))
    yield structs


@sprint3.test
def keywords(structs):
    """End-to-end test headers with lua reserved keywords in them."""
    assert 'keyword_test' in structs
    assert structs['keyword_test']
    assert compare_lua(structs['keyword_test'], '''
    -- Dissector for keyword_test: testing lua keywords
    local proto_keyword_test = Proto("keyword_test", "testing lua keywords")
    -- ProtoField defintions for: keyword_test
    local f = proto_keyword_test.fields
    f._in = ProtoField.int32("keyword_test.in", "in")
    f._until = ProtoField.bytes("keyword_test.until", "until")
    f._until_0 = ProtoField.bytes("keyword_test.until.0", "until[0]")
    f._until_0_0 = ProtoField.int32("keyword_test.until.0.0", "until[0][0]")
    f._until_0_1 = ProtoField.int32("keyword_test.until.0.1", "until[0][1]")
    f._until_1 = ProtoField.bytes("keyword_test.until.1", "until[1]")
    f._until_1_0 = ProtoField.int32("keyword_test.until.1.0", "until[1][0]")
    f._until_1_1 = ProtoField.int32("keyword_test.until.1.1", "until[1][1]")
    f._version = ProtoField.uint32("keyword_test._VERSION", "_VERSION (bitstring)", base.HEX)
    f._version_g1 = ProtoField.uint32("keyword_test._VERSION.G1", "G1", nil, {[0]="True", [1]="False"}, 0x1)
    local function_valuestring = {[1]="and", [2]="elseif", [412]="in"}
    f._function = ProtoField.uint32("keyword_test.function", "function", nil, function_valuestring)
    f._and = ProtoField.int32("keyword_test.and", "and")
    f._and = ProtoField.int32("keyword_test._and", "_and")
    f._not = ProtoField.int32("keyword_test.not", "not")
    -- Dissector function for: keyword_test
    function proto_keyword_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_keyword_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": keyword_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(testing lua keywords)")
    end
    local in_node = subtree:add_le(f._in, buffer(0, 4))
    local in_value = buffer(0, 4):le_int()
    if in_value < 0.0 then
    in_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
    end
    if in_value > 10.0 then
    in_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 10.0")
    end
    local array = subtree:add_le(f._until, buffer(4, 16))
    array:set_text("until (4 x int32)")
    local subarray = array:add_le(f._until_0, buffer(4, 8))
    subarray:set_text("until[0] (2 x int32)")
    subarray:add_le(f._until_0_0, buffer(4, 4))
    subarray:add_le(f._until_0_1, buffer(8, 4))
    local subarray = array:add_le(f._until_1, buffer(12, 8))
    subarray:set_text("until[1] (2 x int32)")
    subarray:add_le(f._until_1_0, buffer(12, 4))
    subarray:add_le(f._until_1_1, buffer(16, 4))
    local bittree = subtree:add_le(f._version, buffer(20, 4))
    bittree:add_le(f._version_g1, buffer(20, 4))
    local function_node = subtree:add_le(f._function, buffer(24, 4))
    local function_value = buffer(24, 4):le_uint()
    if function_valuestring[function_value] == nil then
    function_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 412]")
    end
    pinfo.private.field_name = "or"
    Dissector.get("local"):call(buffer(28, 4):tvb(), pinfo, subtree)
    subtree:add_le(f._and, buffer(32, 4))
    subtree:add_le(f._and, buffer(36, 4))
    subtree:add_le(f._not, buffer(40, 4))
    -- Trailers handling for struct: keyword_test
    local trail_offset = 44
    local trail_count = buffer(40, 4):le_int()
    for i = 1, trail_count do
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset, 5):tvb(), pinfo, tree)
    end
    end
    delegator_register_proto(proto_keyword_test, "keyword_test", 255, {[1]=44})
    ''')


@sprint3.test
def platforms(structs):
    """End-to-end test platform specific header."""
    assert 'platform_test' in structs
    assert structs['platform_test']
    assert compare_lua(structs['platform_test'], '''
    -- Dissector for platform_test: struct platform_test
    local proto_platform_test = Proto("platform_test", "struct platform_test")
    -- ProtoField defintions for: platform_test
    local f = proto_platform_test.fields
    f.bytes = ProtoField.bytes("platform_test.bytes", "bytes")
    f.a = ProtoField.int32("platform_test.a", "a")
    f.win_float = ProtoField.float("platform_test.win_float", "win_float")
    f.b = ProtoField.int8("platform_test.b", "b")
    f.deff = ProtoField.int64("platform_test.deff", "deff")
    f.intel = ProtoField.int64("platform_test.intel", "intel")
    -- Dissector function for: platform_test
    function proto_platform_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_platform_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": platform_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct platform_test)")
    end
    subtree:add_le(f.bytes, buffer(0, 8))
    subtree:add_le(f.a, buffer(8, 4))
    subtree:add_le(f.win_float, buffer(12, 4))
    subtree:add_le(f.b, buffer(16, 1))
    pinfo.private.field_name = "anom"
    Dissector.get("anom"):call(buffer(20, 4):tvb(), pinfo, subtree)
    subtree:add_le(f.deff, buffer(24, 4))
    subtree:add_le(f.intel, buffer(28, 4))
    end
    delegator_register_proto(proto_platform_test, "platform_test", 670, {[1]=32})
    ''')


@sprint3.test
def unions(structs):
    """End-to-end test unions header."""
    assert 'union_test' in structs
    assert structs['union_test']
    assert compare_lua(structs['union_test'], '''
    -- Dissector for union_test: Test for union_test
    local proto_union_test = Proto("union_test", "Test for union_test")
    -- ProtoField defintions for: union_test
    local f = proto_union_test.fields
    f.int_member = ProtoField.int32("union_test.int_member", "int_member")
    f.float_member = ProtoField.float("union_test.float_member", "float_member")
    f.long_long_member = ProtoField.uint64("union_test.long_long_member", "long_long_member")
    -- Dissector function for: union_test
    function proto_union_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_union_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": union_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(Test for union_test)")
    end
    subtree:add_le(f.int_member, buffer(0, 4))
    subtree:add_le(f.float_member, buffer(0, 4))
    subtree:add_le(f.long_long_member, buffer(0, 8))
    end
    delegator_register_proto(proto_union_test, "union_test", 161, {[1]=8})
    ''')


@sprint3.test
def conformance_files(structs):
    """End-to-end test conformance-files."""
    assert 'custom_lua' in structs
    assert structs['custom_lua']
    assert compare_lua(structs['custom_lua'], '''
    -- Dissector for custom_lua: struct custom_lua
    local proto_custom_lua = Proto("custom_lua", "struct custom_lua")
    -- ProtoField defintions for: custom_lua
    local f = proto_custom_lua.fields
    f.normal = ProtoField.int16("custom_lua.normal", "normal")
    f.special = ProtoField.int64("custom_lua.special", "special")
    f.abs = ProtoField.absolute_time("custom_lua.abs", "abs")
    f.rel = ProtoField.relative_time("custom_lua.rel", "rel")
    f.abool = ProtoField.bool("custom_lua.bool", "A BOOL")
    f.something = ProtoField.uint32("custom_lua.all.all", "Something", base.HEX, {[0]="Monday", [1]="Tuesday"}, nil, "This is something dark side!")
    -- This is above 'truth'
    local truth_valuestring = {[0]="TRUE", [1]="FALSE"}
    f.truth = ProtoField.uint32("custom_lua.truth", "truth", nil, truth_valuestring)
    -- This is below
    f.five = ProtoField.bytes("custom_lua.five", "five")
    f.five_0 = ProtoField.int32("custom_lua.five.0", "five[0]")
    f.five_1 = ProtoField.int32("custom_lua.five.1", "five[1]")
    f.five_2 = ProtoField.int32("custom_lua.five.2", "five[2]")
    f.five_3 = ProtoField.int32("custom_lua.five.3", "five[3]")
    f.five_4 = ProtoField.int32("custom_lua.five.4", "five[4]")
    f.pointer = ProtoField.int32("custom_lua.pointer", "pointer")
    -- This is below 'pointer'
    f.str = ProtoField.string("custom_lua.str", "str")
    f.str_0 = ProtoField.string("custom_lua.str.0", "str[0]")
    f.str_0_0 = ProtoField.string("custom_lua.str.0.0", "str[0][0]")
    f.str_0_1 = ProtoField.string("custom_lua.str.0.1", "str[0][1]")
    f.str_0_2 = ProtoField.string("custom_lua.str.0.2", "str[0][2]")
    f.str_1 = ProtoField.string("custom_lua.str.1", "str[1]")
    f.str_1_0 = ProtoField.string("custom_lua.str.1.0", "str[1][0]")
    f.str_1_1 = ProtoField.string("custom_lua.str.1.1", "str[1][1]")
    f.str_1_2 = ProtoField.string("custom_lua.str.1.2", "str[1][2]")
    f.str_2 = ProtoField.string("custom_lua.str.2", "str[2]")
    f.str_2_0 = ProtoField.string("custom_lua.str.2.0", "str[2][0]")
    f.str_2_1 = ProtoField.string("custom_lua.str.2.1", "str[2][1]")
    f.str_2_2 = ProtoField.string("custom_lua.str.2.2", "str[2][2]")
    f.str_3 = ProtoField.string("custom_lua.str.3", "str[3]")
    f.str_3_0 = ProtoField.string("custom_lua.str.3.0", "str[3][0]")
    f.str_3_1 = ProtoField.string("custom_lua.str.3.1", "str[3][1]")
    f.str_3_2 = ProtoField.string("custom_lua.str.3.2", "str[3][2]")
    -- This was all the field defintions
    -- Dissector function for: custom_lua
    function proto_custom_lua.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_custom_lua, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": custom_lua")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct custom_lua)")
    end
    subtree:add_le(f.normal, buffer(0, 2))
    subtree:add_le(f.special, buffer(8, 8))
    subtree:add_le(f.abs, buffer(16, 4))
    subtree:add_le(f.rel, buffer(20, 4))
    subtree:add_le(f.abool, buffer(24, 4))
    subtree:add_le(f.something, buffer(28, 4))
    -- This is above 'truth' inside the dissector function.
    local truth_node = subtree:add_le(f.truth, buffer(32, 4))
    local truth_value = buffer(32, 4):le_uint()
    if truth_valuestring[truth_value] == nil then
    truth_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1]")
    end
    local field_value_var = subtree:add_le(f.five, buffer(36, 20))
    field_value_var:set_text("five (5 x int32)")
    field_value_var:add_le(f.five_0, buffer(36, 4))
    field_value_var:add_le(f.five_1, buffer(40, 4))
    field_value_var:add_le(f.five_2, buffer(44, 4))
    field_value_var:add_le(f.five_3, buffer(48, 4))
    field_value_var:add_le(f.five_4, buffer(52, 4))
    -- This is below 'five' inside dissector function
    -- Offset: 36 and field_value_var variable.
    subtree:add_le(f.pointer, buffer(56, 4))
    --[[ This comments out the str array code
    local array = subtree:add_le(f.str, buffer(60, 24))
    local subarray = array:add_le(f.str_0, buffer(60, 6))
    subarray:add_le(f.str_0_0, buffer(60, 2))
    subarray:add_le(f.str_0_1, buffer(62, 2))
    subarray:add_le(f.str_0_2, buffer(64, 2))
    local subarray = array:add_le(f.str_1, buffer(66, 6))
    subarray:add_le(f.str_1_0, buffer(66, 2))
    subarray:add_le(f.str_1_1, buffer(68, 2))
    subarray:add_le(f.str_1_2, buffer(70, 2))
    local subarray = array:add_le(f.str_2, buffer(72, 6))
    subarray:add_le(f.str_2_0, buffer(72, 2))
    subarray:add_le(f.str_2_1, buffer(74, 2))
    subarray:add_le(f.str_2_2, buffer(76, 2))
    local subarray = array:add_le(f.str_3, buffer(78, 6))
    subarray:add_le(f.str_3_0, buffer(78, 2))
    subarray:add_le(f.str_3_1, buffer(80, 2))
    subarray:add_le(f.str_3_2, buffer(82, 2))
    ]]--
    -- This is the last line of the dissector function
    end
    delegator_register_proto(proto_custom_lua, "custom_lua", 74, {[1]=88})
    ''')


# End-to-end tests for sprint 4 features
sprint4 = Tests()

@sprint4.context
def create_sprint4():
    """Create protocols for all structs in sprint2.h"""
    headers = [os.path.join(os.path.dirname(__file__), i)
                for i in ['sprint4.h', 'a.h', 'b.h']]
    yml = os.path.join(os.path.dirname(__file__), 'sprint4.yml')
    args = ['-v', '-d', '-I', os.path.dirname(__file__)]
    protos, defaults = create_protocols(headers, yml, args, cleanup=False)
    yield protos
    perform_cleanup(defaults)


@sprint4.test
def enum_arrays(structs):
    """Test support for arrays of enums."""
    assert 'enum_arrays' in structs
    assert structs['enum_arrays']
    assert compare_lua(structs['enum_arrays'], '''
    -- Dissector for enum_arrays: struct enum_arrays
    local proto_enum_arrays = Proto("enum_arrays", "struct enum_arrays")
    -- ProtoField defintions for: enum_arrays
    local f = proto_enum_arrays.fields
    f.month_array = ProtoField.bytes("enum_arrays.month_array", "month_array")
    local month_array_valuestring = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="NOV", [20]="DEC"}
    f.month_array_0 = ProtoField.uint32("enum_arrays.month_array.0", "month_array[0]", nil, month_array_valuestring)
    local month_array_valuestring = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="NOV", [20]="DEC"}
    f.month_array_1 = ProtoField.uint32("enum_arrays.month_array.1", "month_array[1]", nil, month_array_valuestring)
    local month_array_valuestring = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="NOV", [20]="DEC"}
    f.month_array_2 = ProtoField.uint32("enum_arrays.month_array.2", "month_array[2]", nil, month_array_valuestring)
    local month_array_valuestring = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="NOV", [20]="DEC"}
    f.month_array_3 = ProtoField.uint32("enum_arrays.month_array.3", "month_array[3]", nil, month_array_valuestring)
    -- Dissector function for: enum_arrays
    function proto_enum_arrays.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_enum_arrays, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": enum_arrays")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct enum_arrays)")
    end
    local array = subtree:add_le(f.month_array, buffer(0, 16))
    array:set_text("month_array (4 x uint32)")
    local month_array_node = array:add_le(f.month_array_0, buffer(0, 4))
    local month_array_value = buffer(0, 4):le_uint()
    if month_array_valuestring[month_array_value] == nil then
    month_array_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 3, 4, 5, 20]")
    end
    local month_array_node = array:add_le(f.month_array_1, buffer(4, 4))
    local month_array_value = buffer(4, 4):le_uint()
    if month_array_valuestring[month_array_value] == nil then
    month_array_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 3, 4, 5, 20]")
    end
    local month_array_node = array:add_le(f.month_array_2, buffer(8, 4))
    local month_array_value = buffer(8, 4):le_uint()
    if month_array_valuestring[month_array_value] == nil then
    month_array_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 3, 4, 5, 20]")
    end
    local month_array_node = array:add_le(f.month_array_3, buffer(12, 4))
    local month_array_value = buffer(12, 4):le_uint()
    if month_array_valuestring[month_array_value] == nil then
    month_array_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [1, 2, 3, 4, 5, 20]")
    end
    end
    delegator_register_proto(proto_enum_arrays, "enum_arrays", nil, {[1]=16})
    ''')


@sprint4.test
def cpp_arguments(structs):
    """Test support for providing CPP arguments from config."""
    assert 'cpp_test' in structs
    assert structs['cpp_test']
    assert compare_lua(structs['cpp_test'], '''
    -- Dissector for cpp_test: struct cpp_test
    local proto_cpp_test = Proto("cpp_test", "struct cpp_test")
    -- ProtoField defintions for: cpp_test
    local f = proto_cpp_test.fields
    f.arr = ProtoField.bytes("cpp_test.arr", "arr")
    f.arr_0 = ProtoField.bytes("cpp_test.arr.0", "arr[0]")
    f.arr_0_0 = ProtoField.bytes("cpp_test.arr.0.0", "arr[0][0]")
    f.arr_0_1 = ProtoField.bytes("cpp_test.arr.0.1", "arr[0][1]")
    f.arr_0_2 = ProtoField.bytes("cpp_test.arr.0.2", "arr[0][2]")
    f.arr_1 = ProtoField.bytes("cpp_test.arr.1", "arr[1]")
    f.arr_1_0 = ProtoField.bytes("cpp_test.arr.1.0", "arr[1][0]")
    f.arr_1_1 = ProtoField.bytes("cpp_test.arr.1.1", "arr[1][1]")
    f.arr_1_2 = ProtoField.bytes("cpp_test.arr.1.2", "arr[1][2]")
    f.test = ProtoField.float("cpp_test.test", "test")
    -- Dissector function for: cpp_test
    function proto_cpp_test.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add_le(proto_cpp_test, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": cpp_test")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(struct cpp_test)")
    end
    local array = subtree:add_le(f.arr, buffer(0, 48))
    array:set_text("arr (6 x bytes)")
    local subarray = array:add_le(f.arr_0, buffer(0, 24))
    subarray:set_text("arr[0] (3 x bytes)")
    subarray:add_le(f.arr_0_0, buffer(0, 8))
    subarray:add_le(f.arr_0_1, buffer(8, 8))
    subarray:add_le(f.arr_0_2, buffer(16, 8))
    local subarray = array:add_le(f.arr_1, buffer(24, 24))
    subarray:set_text("arr[1] (3 x bytes)")
    subarray:add_le(f.arr_1_0, buffer(24, 8))
    subarray:add_le(f.arr_1_1, buffer(32, 8))
    subarray:add_le(f.arr_1_2, buffer(40, 8))
    subtree:add_le(f.test, buffer(48, 4))
    end
    delegator_register_proto(proto_cpp_test, "cpp_test", 10, {[1]=52})
    delegator_register_proto(proto_cpp_test, "cpp_test", 12, {[1]=52})
    delegator_register_proto(proto_cpp_test, "cpp_test", 14, {[1]=52})
    ''')


@sprint4.test
def placeholder_configs(structs):
    """Test that it works to generate placeholder configs."""
    protocols = cparser.StructVisitor.all_protocols
    assert protocols
    text, count = config.generate_placeholders(protocols)
    assert text and count
    assert count == 3
    assert text.startswith('Options:')

