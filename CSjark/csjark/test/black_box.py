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


# End-to-end tests for sprint 2 features
sprint2 = Tests()

@sprint2.context
def create_protocols():
    """Create protocols for all structs in sprint2.h"""
    c = csjark.Cli
    defaults = c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file

    # Parse command line arguments
    header = os.path.join(os.path.dirname(__file__), 'sprint2.h')
    yml = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
    headers, configs = c.parse_args(['-i', header, '-c', yml])

    # Parse config files
    for filename in configs:
        config.parse_file(filename)

    # Create dissectors
    structs = {}
    for header in headers:
        ast = cparser.parse_file(header, use_cpp=True)
        protocols = cparser.find_structs(ast)
        for proto in protocols:
            structs[proto.name] = proto.create()

    yield structs

    # Write out dissectors for manual testing
    if True:
        path = os.path.dirname(__file__)
        for name, code in structs.items():
            with open('%s/%s.lua' % (path, name), 'w') as f:
                f.write(code)

    # Clean up context
    del structs
    cparser.StructVisitor.all_structs = {}
    config.StructConfig.configs = {}
    c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file = defaults


@sprint2.test
def arrays(structs):
    """End-to-end test headers with arrays in them."""
    assert 'array_test' in structs
    assert structs['array_test']
    assert compare_lua(structs['array_test'], '''
    -- Dissector for struct: array_test: Multidimensional array
    local proto_array_test = Proto("array_test", "Multidimensional array")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: array_test
    local f = proto_array_test.fields
    f.chararr1 = ProtoField.string("array_test.chararr1", "chararr1")
    -- Array definition for intarr2
    f.intarr2_0 = ProtoField.bytes("array_test.intarr2", "intarr2")
    f.intarr2_1 = ProtoField.bytes("array_test.intarr2", "intarr2")
    f.intarr2_2 = ProtoField.bytes("array_test.intarr2", "intarr2")
    f.intarr2_3 = ProtoField.bytes("array_test.intarr2", "intarr2")
    f.intarr2__0 = ProtoField.int32("array_test.intarr2.0", "[0]")
    f.intarr2__1 = ProtoField.int32("array_test.intarr2.1", "[1]")
    f.intarr2__2 = ProtoField.int32("array_test.intarr2.2", "[2]")
    f.intarr2__3 = ProtoField.int32("array_test.intarr2.3", "[3]")
    f.intarr2__4 = ProtoField.int32("array_test.intarr2.4", "[4]")
    f.intarr2__5 = ProtoField.int32("array_test.intarr2.5", "[5]")
    f.intarr2__6 = ProtoField.int32("array_test.intarr2.6", "[6]")
    f.intarr2__7 = ProtoField.int32("array_test.intarr2.7", "[7]")
    f.intarr2__8 = ProtoField.int32("array_test.intarr2.8", "[8]")
    f.intarr2__9 = ProtoField.int32("array_test.intarr2.9", "[9]")
    f.intarr2__10 = ProtoField.int32("array_test.intarr2.10", "[10]")
    f.intarr2__11 = ProtoField.int32("array_test.intarr2.11", "[11]")
    f.intarr2__12 = ProtoField.int32("array_test.intarr2.12", "[12]")
    f.intarr2__13 = ProtoField.int32("array_test.intarr2.13", "[13]")
    f.intarr2__14 = ProtoField.int32("array_test.intarr2.14", "[14]")
    f.intarr2__15 = ProtoField.int32("array_test.intarr2.15", "[15]")
    -- Array definition for chararr3
    f.chararr3_0 = ProtoField.string("array_test.chararr3", "chararr3")
    f.chararr3_1 = ProtoField.string("array_test.chararr3", "chararr3")
    f.chararr3__0 = ProtoField.string("array_test.chararr3.0", "[0]")
    f.chararr3__1 = ProtoField.string("array_test.chararr3.1", "[1]")
    -- Array definition for floatarr4
    f.floatarr4_0 = ProtoField.bytes("array_test.floatarr4", "floatarr4")
    f.floatarr4_1 = ProtoField.bytes("array_test.floatarr4", "floatarr4")
    f.floatarr4__0 = ProtoField.float("array_test.floatarr4.0", "[0]")
    f.floatarr4__1 = ProtoField.float("array_test.floatarr4.1", "[1]")
    f.floatarr4__2 = ProtoField.float("array_test.floatarr4.2", "[2]")
    f.floatarr4__3 = ProtoField.float("array_test.floatarr4.3", "[3]")
    f.floatarr4__4 = ProtoField.float("array_test.floatarr4.4", "[4]")
    f.floatarr4__5 = ProtoField.float("array_test.floatarr4.5", "[5]")
    -- Dissector function for struct: array_test
    function proto_array_test.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_array_test, buffer())
    pinfo.cols.info:append(" (" .. proto_array_test.description .. ")")
    subtree:add(f.chararr1, buffer(0, 16))
    -- Array handling for intarr2
    local arraytree = subtree:add(f.intarr2_0, buffer(16, 64))
    arraytree:set_text("intarr2 (array: 16 x int32)")
    local subarraytree = arraytree:add(f.intarr2_1, buffer(16, 16))
    subarraytree:set_text("(array: 4 x int32)")
    subarraytree:add(f.intarr2__0, buffer(16, 4))
    subarraytree:add(f.intarr2__1, buffer(20, 4))
    subarraytree:add(f.intarr2__2, buffer(24, 4))
    subarraytree:add(f.intarr2__3, buffer(28, 4))
    local subarraytree = arraytree:add(f.intarr2_2, buffer(32, 16))
    subarraytree:set_text("(array: 4 x int32)")
    subarraytree:add(f.intarr2__4, buffer(32, 4))
    subarraytree:add(f.intarr2__5, buffer(36, 4))
    subarraytree:add(f.intarr2__6, buffer(40, 4))
    subarraytree:add(f.intarr2__7, buffer(44, 4))
    local subarraytree = arraytree:add(f.intarr2_3, buffer(48, 16))
    subarraytree:set_text("(array: 4 x int32)")
    subarraytree:add(f.intarr2__8, buffer(48, 4))
    subarraytree:add(f.intarr2__9, buffer(52, 4))
    subarraytree:add(f.intarr2__10, buffer(56, 4))
    subarraytree:add(f.intarr2__11, buffer(60, 4))
    local subarraytree = arraytree:add(f.intarr2_4, buffer(64, 16))
    subarraytree:set_text("(array: 4 x int32)")
    subarraytree:add(f.intarr2__12, buffer(64, 4))
    subarraytree:add(f.intarr2__13, buffer(68, 4))
    subarraytree:add(f.intarr2__14, buffer(72, 4))
    subarraytree:add(f.intarr2__15, buffer(76, 4))
    -- Array handling for chararr3
    local arraytree = subtree:add(f.chararr3_0, buffer(80, 6))
    arraytree:set_text("chararr3 (array: 2 x string)")
    arraytree:add(f.chararr3__0, buffer(80, 3))
    arraytree:add(f.chararr3__1, buffer(83, 3))
    -- Array handling for floatarr4
    local arraytree = subtree:add(f.floatarr4_0, buffer(86, 24))
    arraytree:set_text("floatarr4 (array: 6 x float)")
    local subarraytree = arraytree:add(f.floatarr4_1, buffer(86, 12))
    subarraytree:set_text("(array: 3 x float)")
    subarraytree:add(f.floatarr4__0, buffer(86, 4))
    subarraytree:add(f.floatarr4__1, buffer(90, 4))
    subarraytree:add(f.floatarr4__2, buffer(94, 4))
    local subarraytree = arraytree:add(f.floatarr4_2, buffer(98, 12))
    subarraytree:set_text("(array: 3 x float)")
    subarraytree:add(f.floatarr4__3, buffer(98, 4))
    subarraytree:add(f.floatarr4__4, buffer(102, 4))
    subarraytree:add(f.floatarr4__5, buffer(106, 4))
    end
    luastructs_dt:add(16, proto_array_test)
    ''')


@sprint2.test
def bitstrings(structs):
    """End-to-end test headers with bitstrings in them."""
    assert 'bitstring_test' in structs
    assert structs['bitstring_test']
    assert compare_lua(structs['bitstring_test'], '''
    -- Dissector for struct: bitstring_test: Bit string test
    local proto_bitstring_test = Proto("bitstring_test", "Bit string test")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: bitstring_test
    local f = proto_bitstring_test.fields
    f.id = ProtoField.int32("bitstring_test.id", "id")
    -- Bitstring definitions for flags
    f.flags = ProtoField.uint32("bitstring_test.flags", "flags (bitstring)", base.HEX)
    f.flags_Inuse = ProtoField.uint32("bitstring_test.flags.In_use", "In use", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.flags_Endian = ProtoField.uint32("bitstring_test.flags.Endian", "Endian", nil, {[0]="Big", [1]="Little"}, 0x2)
    f.flags_Platform = ProtoField.uint32("bitstring_test.flags.Platform", "Platform", nil, {[0]="Win", [1]="Linux", [2]="Mac", [3]="Solaris"}, 0xc)
    f.flags_Test = ProtoField.uint32("bitstring_test.flags.Test", "Test", nil, {[0]="No", [1]="Yes"}, 0x10)
    -- Bitstring definitions for color1
    f.color1 = ProtoField.uint16("bitstring_test.color1", "color1 (bitstring)", base.HEX)
    f.color1_RED = ProtoField.uint16("bitstring_test.color1.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.color1_Blue = ProtoField.uint16("bitstring_test.color1.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.color1_Green = ProtoField.uint16("bitstring_test.color1.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
    -- Bitstring definitions for color2
    f.color2 = ProtoField.uint16("bitstring_test.color2", "color2 (bitstring)", base.HEX)
    f.color2_RED = ProtoField.uint16("bitstring_test.color2.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.color2_Blue = ProtoField.uint16("bitstring_test.color2.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.color2_Green = ProtoField.uint16("bitstring_test.color2.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
    -- Dissector function for struct: bitstring_test
    function proto_bitstring_test.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_bitstring_test, buffer())
    pinfo.cols.info:append(" (" .. proto_bitstring_test.description .. ")")
    subtree:add(f.id, buffer(0, 4))
    -- Bitstring handling for flags
    local bittree = subtree:add(f.flags, buffer(4, 4))
    bittree:add(f.flags_Inuse, buffer(4, 4))
    bittree:add(f.flags_Endian, buffer(4, 4))
    bittree:add(f.flags_Platform, buffer(4, 4))
    bittree:add(f.flags_Test, buffer(4, 4))
    -- Bitstring handling for color1
    local bittree = subtree:add(f.color1, buffer(8, 2))
    bittree:add(f.color1_RED, buffer(8, 2))
    bittree:add(f.color1_Blue, buffer(8, 2))
    bittree:add(f.color1_Green, buffer(8, 2))
    -- Bitstring handling for color2
    local bittree = subtree:add(f.color2, buffer(10, 2))
    bittree:add(f.color2_RED, buffer(10, 2))
    bittree:add(f.color2_Blue, buffer(10, 2))
    bittree:add(f.color2_Green, buffer(10, 2))
    end
    luastructs_dt:add(13, proto_bitstring_test)
    ''')


@sprint2.test
def cenums(structs):
    """End-to-end test headers with C enums in them."""
    assert 'cenum_test' in structs
    assert structs['cenum_test']
    assert compare_lua(structs['cenum_test'], '''
    -- Dissector for struct: cenum_test: C Enum test
    local proto_cenum_test = Proto("cenum_test", "C Enum test")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: cenum_test
    local f = proto_cenum_test.fields
    f.id = ProtoField.int32("cenum_test.id", "id")
    f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, {[1]="JAN", [2]="FEB",
    [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"})
    -- Dissector function for struct: cenum_test
    function proto_cenum_test.dissector(buffer, pinfo, tree)
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


@sprint2.test
def custom(structs):
    """End-to-end test headers with custom field rules."""
    assert 'custom_lua' in structs
    assert structs['custom_lua']
    assert compare_lua(structs['custom_lua'], '''
    -- Dissector for struct: custom_lua: struct custom_lua
    local proto_custom_lua = Proto("custom_lua", "struct custom_lua")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: custom_lua
    local f = proto_custom_lua.fields
    f.normal = ProtoField.int16("custom_lua.normal", "normal")
    f.special = ProtoField.int64("custom_lua.special", "special")
    f.abs = ProtoField.absolute_time("None", "abs")
    f.rel = ProtoField.relative_time("None", "rel")
    f.bol = ProtoField.bool("bool", "bol")
    f.all = ProtoField.uint32("all.all", "all", base.HEX, {[0]="Monday", [1]="Tuesday"}, nil, "This is something dark side!")
    -- Dissector function for struct: custom_lua
    function proto_custom_lua.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_custom_lua, buffer())
    pinfo.cols.info:append(" (" .. proto_custom_lua.description .. ")")
    subtree:add(f.normal, buffer(0, 2))
    subtree:add(f.special, buffer(2, 8))
    subtree:add(f.abs, buffer(10, 4))
    subtree:add(f.rel, buffer(14, 4))
    subtree:add(f.bol, buffer(18, 4))
    subtree:add(f.all, buffer(22, 4))
    end
    luastructs_dt:add(74, proto_custom_lua)
    ''')


@sprint2.test
def enums(structs):
    """End-to-end test headers with enums in them."""
    assert 'enum_test' in structs
    assert structs['enum_test']
    assert compare_lua(structs['enum_test'], '''
    -- Dissector for struct: enum_test: Enum config test
    local proto_enum_test = Proto("enum_test", "Enum config test")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: enum_test
    local f = proto_enum_test.fields
    f.id = ProtoField.int32("enum_test.id", "id", nil, {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"})
    f.name = ProtoField.string("enum_test.name", "name")
    f.weekday = ProtoField.int32("enum_test.weekday", "weekday", nil, {[1]="MONDAY", [2]="TUESDAY", [3]="WEDNESDAY", [4]="THURSDAY", [5]="FRIDAY", [6]="SATURDAY", [7]="SUNDAY"})
    f.number = ProtoField.int32("enum_test.number", "number", nil, {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"})
    -- Dissector function for struct: enum_test
    function proto_enum_test.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_enum_test, buffer())
    pinfo.cols.info:append(" (" .. proto_enum_test.description .. ")")
    local id = subtree:add(f.id, buffer(0, 4))
    local test = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
    if (test[buffer(0, 4):int()] == nil) then
    id:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1, 2, 3, 4, 5)")
    end
    subtree:add(f.name, buffer(4, 10))
    local weekday = subtree:add(f.weekday, buffer(14, 4))
    local test = {[1]="MONDAY", [2]="TUESDAY", [3]="WEDNESDAY", [4]="THURSDAY", [5]="FRIDAY", [6]="SATURDAY", [7]="SUNDAY"}
    if (test[buffer(14, 4):int()] == nil) then
    weekday:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7)")
    end
    local number = subtree:add(f.number, buffer(18, 4))
    local test = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
    if (test[buffer(18, 4):int()] == nil) then
    number:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1, 2, 3, 4, 5)")
    end
    end
    luastructs_dt:add(10, proto_enum_test)
    ''')


@sprint2.test
def ranges(structs):
    """End-to-end test headers with ranges in them."""
    assert 'range_test' in structs
    assert structs['range_test']
    assert compare_lua(structs['range_test'], '''
    -- Dissector for struct: range_test: Range rules test
    local proto_range_test = Proto("range_test", "Range rules test")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: range_test
    local f = proto_range_test.fields
    f.name = ProtoField.string("range_test.name", "name")
    f.age = ProtoField.int32("range_test.age", "age")
    -- Dissector function for struct: range_test
    function proto_range_test.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_range_test, buffer())
    pinfo.cols.info:append(" (" .. proto_range_test.description .. ")")
    subtree:add(f.name, buffer(0, 10))
    local age = subtree:add(f.age, buffer(10, 4))
    if (buffer(10, 4):int() < 0.0) then
    age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
    end
    if (buffer(10, 4):int() > 100.0) then
    age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 100.0")
    end
    end
    luastructs_dt:add(9, proto_range_test)
    ''')


@sprint2.test
def trailers(structs):
    """End-to-end test headers with trailers in them."""
    assert 'trailer_test' in structs
    assert structs['trailer_test']
    assert compare_lua(structs['trailer_test'], '''
    -- Dissector for struct: trailer_test: struct trailer_test
    local proto_trailer_test = Proto("trailer_test", "struct trailer_test")
    local luastructs_dt = DissectorTable.get("luastructs.message")
    -- ProtoField defintions for struct: trailer_test
    local f = proto_trailer_test.fields
    -- Array definition for tmp
    f.tmp_0 = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp_1 = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp_2 = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp_3 = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp_4 = ProtoField.bytes("trailer_test.tmp", "tmp")
    f.tmp__0 = ProtoField.float("trailer_test.tmp.0", "[0]")
    f.tmp__1 = ProtoField.float("trailer_test.tmp.1", "[1]")
    f.tmp__2 = ProtoField.float("trailer_test.tmp.2", "[2]")
    f.tmp__3 = ProtoField.float("trailer_test.tmp.3", "[3]")
    f.tmp__4 = ProtoField.float("trailer_test.tmp.4", "[4]")
    f.asn1_count = ProtoField.int32("trailer_test.asn1_count", "asn1_count")
    -- Dissector function for struct: trailer_test
    function proto_trailer_test.dissector(buffer, pinfo, tree)
    local subtree = tree:add(proto_trailer_test, buffer())
    pinfo.cols.info:append(" (" .. proto_trailer_test.description .. ")")
    -- Array handling for tmp
    local arraytree = subtree:add(f.tmp_0, buffer(0, 20))
    arraytree:set_text("tmp (array: 5 x float)")
    arraytree:add(f.tmp__0, buffer(0, 4))
    arraytree:add(f.tmp__1, buffer(4, 4))
    arraytree:add(f.tmp__2, buffer(8, 4))
    arraytree:add(f.tmp__3, buffer(12, 4))
    arraytree:add(f.tmp__4, buffer(16, 4))
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
    luastructs_dt:add(66, proto_trailer_test)
    ''')

