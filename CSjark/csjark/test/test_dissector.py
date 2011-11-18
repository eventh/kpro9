# -*- coding: utf-8 -*-
# Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
# Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
# Sigurd Wien and Jaroslav Fibichr.
#
# This file is part of CSjark.
#
# CSjark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSjark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSjark.  If not, see <http://www.gnu.org/licenses/>.
"""
Module for testing the dissector module.

Tests the output of generating dissectors.
"""
import sys, os
from attest import Tests, assert_hook, contexts

import dissector
from field import Field, ArrayField, ProtocolField, BitField
from config import Config, Trailer
from platform import Platform


def compare_lua(code, template, write_to_file=''):
    """Test that generated lua code equals what is expected."""
    if write_to_file:
        with open(write_to_file, 'a') as f:
            f.write('%s\n' % code.replace('\t',''))
    def simplify(text):
        return ''.join(text.strip().split())
    return simplify(code) == simplify(template)


# Test EnumField
enums = Tests()

@enums.context
def create_enum_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    field = Field('enum', 'int32', 4, 0, Platform.big)
    field.set_list_validation(dict(enumerate('ABCDE')))
    diss.add_field(field)
    diss.push_modifiers()
    yield diss.children[0]
    dissector.Protocol.protocols = {}
    del proto, diss

@enums.test
def enum_def(field):
    """Test that EnumField generates valid defintion code."""
    assert field
    assert compare_lua(field.get_definition(), '''
    local enum_valuestring = {[0]="A", [1]="B", [2]="C", [3]="D", [4]="E"}
    f.enum = ProtoField.int32("test.enum", "enum", nil, enum_valuestring)
    ''')

@enums.test
def enum_code(field):
    """Test that EnumField generates correct code."""
    assert isinstance(field, Field)
    assert compare_lua(field.get_code(0), '''
    local enum_node = subtree:add(f.enum, buffer(0, 4))
    local enum_value = buffer(0, 4):int()
    if enum_valuestring[enum_value] == nil then
    enum_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4]")
    end
    ''')


# Test Lua Keywords
lua_keywords = Tests()

@lua_keywords.context
def create_lua_keywords_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    field = Field('elseif', 'int32', 4, 0, Platform.big)
    field.set_list_validation(dict(enumerate('VWXYZ')))
    diss.add_field(field)
    diss.add_field(Field('in', 'float', 4, 0, Platform.big))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@lua_keywords.test
def lua_keywords_def(field1, field2):
    """Test that Lua keyword handling generates valid defintion code."""
    assert field1 and field2
    assert compare_lua(field1.get_definition(), '''
    local elseif_valuestring = {[0]="V", [1]="W", [2]="X", [3]="Y", [4]="Z"}
    f._elseif = ProtoField.int32("test.elseif", "elseif", nil, elseif_valuestring)
    ''')
    assert compare_lua(field2.get_definition(), '''
    f._in = ProtoField.float("test.in", "in")
    ''')

@lua_keywords.test
def lua_keywords_code(field1, field2):
    """Test that the Lua keywords are handled."""
    assert compare_lua(field1.get_code(0), '''
    local elseif_node = subtree:add(f._elseif, buffer(0, 4))
    local elseif_value = buffer(0, 4):int()
    if elseif_valuestring[elseif_value] == nil then
    elseif_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4]")
    end
    ''')
    assert compare_lua(field2.get_code(0), 'subtree:add(f._in, buffer(0, 4))')

@lua_keywords.test
def fields_not_equal(field1, field2):
    """Test that two different fields are not equal."""
    assert field1
    assert field2
    assert field1 == field1
    assert field1 != field2


# Test ArrayField
arrays = Tests()

@arrays.context
def create_array_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    field = Field('arr', 'float', 4, 0, Platform.big)
    diss.add_field(ArrayField.create([2, 3], field))
    field = Field('str', 'string', 30, 0, Platform.big)
    diss.add_field(ArrayField.create([2], field))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@arrays.test
def arrays_def(one, two):
    """Test that ArrayField generates valid defintion code."""
    assert one and two
    assert compare_lua(one.get_definition(), '''
    f.arr = ProtoField.bytes("test.arr", "arr")
    f.arr_0 = ProtoField.bytes("test.arr.0", "arr[0]")
    f.arr_0_0 = ProtoField.float("test.arr.0.0", "arr[0][0]")
    f.arr_0_1 = ProtoField.float("test.arr.0.1", "arr[0][1]")
    f.arr_0_2 = ProtoField.float("test.arr.0.2", "arr[0][2]")
    f.arr_1 = ProtoField.bytes("test.arr.1", "arr[1]")
    f.arr_1_0 = ProtoField.float("test.arr.1.0", "arr[1][0]")
    f.arr_1_1 = ProtoField.float("test.arr.1.1", "arr[1][1]")
    f.arr_1_2 = ProtoField.float("test.arr.1.2", "arr[1][2]")
    ''')
    assert compare_lua(two.get_definition(), '''
    f.str = ProtoField.string("test.str", "str")
    f.str_0 = ProtoField.string("test.str.0", "str[0]")
    f.str_1 = ProtoField.string("test.str.1", "str[1]")
    ''')

@arrays.test
def arrays_code(one, two):
    """Test that ArrayField generates correct code."""
    assert isinstance(one, ArrayField)
    assert compare_lua(one.get_code(0), '''
    local array = subtree:add(f.arr, buffer(0, 24))
    array:set_text("arr (6 x float)")
    local subarray = array:add(f.arr_0, buffer(0, 12))
    subarray:set_text("arr[0] (3 x float)")
    subarray:add(f.arr_0_0, buffer(0, 4))
    subarray:add(f.arr_0_1, buffer(4, 4))
    subarray:add(f.arr_0_2, buffer(8, 4))
    local subarray = array:add(f.arr_1, buffer(12, 12))
    subarray:set_text("arr[1] (3 x float)")
    subarray:add(f.arr_1_0, buffer(12, 4))
    subarray:add(f.arr_1_1, buffer(16, 4))
    subarray:add(f.arr_1_2, buffer(20, 4))
    ''')

@arrays.test
def arrays_str(one, two):
    """Test that ArrayField generates code for char array."""
    assert isinstance(two, ArrayField)
    assert compare_lua(two.get_code(0), '''
    local array = subtree:add(f.str, buffer(0, 60))
    array:add(f.str_0, buffer(0, 30))
    array:add(f.str_1, buffer(30, 30))
    ''')

@arrays.test
def subtrees_not_equal(field1, field2):
    """Test that two different subtree-fields are not equal."""
    assert field1
    assert field2
    assert field1 == field1
    assert field1 != field2

# Test ProtocolField
protofields = Tests()

@protofields.context
def create_protocol_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    proto_one, diss_one = dissector.Protocol.create_dissector('one')
    proto_two, diss_two = dissector.Protocol.create_dissector('two')
    diss.add_field(ProtocolField('test', diss_one))
    diss.add_field(ProtocolField('test2', diss_two))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@protofields.test
def proto_field_def(one, two):
    """Test that ProtocolField generates no defintion code."""
    assert one and two
    assert one.get_definition() is None
    assert two.get_definition() is None

@protofields.test
def proto_field_code(one, two):
    """Test that ProtocolField generates correct code."""
    assert isinstance(one, ProtocolField)
    assert isinstance(two, ProtocolField)
    assert compare_lua(one.get_code(0), '''
    pinfo.private.field_name = "test"
    Dissector.get("one"):call(buffer(0, 0):tvb(), pinfo, subtree)
    ''')
    assert compare_lua(two.get_code(32), '''
    pinfo.private.field_name = "test2"
    Dissector.get("two"):call(buffer(32,0):tvb(), pinfo, subtree)
    ''')

# Test ProtocolField
union_protofields = Tests()

@union_protofields.context
def create_union_protocol_field():
    """Create a Union Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    tmp, one = dissector.Protocol.create_dissector('union_one', union=True)
    tmp, two = dissector.Protocol.create_dissector('union_two', union=True)
    diss.add_field(ProtocolField('test1', one))
    diss.add_field(ProtocolField('test2', two))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@union_protofields.test
def union_proto_field_def(one, two):
    """Test that ProtocolField generates no defintion code."""
    assert one and two
    assert one.get_definition() is None
    assert two.get_definition() is None

@union_protofields.test
def union_proto_field_code(one, two):
    """Test that ProtocolField generates correct code."""
    assert isinstance(one, ProtocolField)
    assert isinstance(two, ProtocolField)
    assert compare_lua(one.get_code(0), '''
    pinfo.private.field_name = "test1"
    Dissector.get("union_one"):call(buffer(0,0):tvb(), pinfo, subtree)
    ''')
    assert compare_lua(two.get_code(32), '''
    pinfo.private.field_name = "test2"
    Dissector.get("union_two"):call(buffer(32,0):tvb(), pinfo, subtree)
    ''')

# Test BitField
bits = Tests()

@bits.context
def create_bit_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    bits = [(1, 1, 'R', {0: 'No', 1: 'Yes'}),
            (2, 1, 'B', {0: 'No', 1: 'Yes'}),
            (3, 1, 'G', {0: 'No', 1: 'Yes'})]
    diss.add_field(BitField(bits, 'bit1', 'int32', 4, 0, Platform.big))
    diss.add_field(BitField(bits, 'bit2', 'uint16', 2, 0, Platform.big))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@bits.test
def bitfield_def(one, two):
    """Test that BitField generates valid defintion code."""
    assert one and two
    assert compare_lua(one.get_definition(), '''
    f.bit1 = ProtoField.uint32("test.bit1", "bit1 (bitstring)", base.HEX)
    f.bit1_r = ProtoField.uint32("test.bit1.R", "R", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.bit1_b = ProtoField.uint32("test.bit1.B", "B", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.bit1_g = ProtoField.uint32("test.bit1.G", "G", nil, {[0]="No", [1]="Yes"}, 0x4)
    ''')
    assert compare_lua(two.get_definition(), '''
    f.bit2 = ProtoField.uint16("test.bit2", "bit2 (bitstring)", base.HEX)
    f.bit2_r = ProtoField.uint16("test.bit2.R", "R", nil, {[0]="No", [1]="Yes"}, 0x1)
    f.bit2_b = ProtoField.uint16("test.bit2.B", "B", nil, {[0]="No", [1]="Yes"}, 0x2)
    f.bit2_g = ProtoField.uint16("test.bit2.G", "G", nil, {[0]="No", [1]="Yes"}, 0x4)
    ''')

@bits.test
def bitfield_code(one, two):
    """Test that BitField generates valid code."""
    assert compare_lua(one.get_code(0), '''
    local bittree = subtree:add(f.bit1, buffer(0, 4))
    bittree:add(f.bit1_r, buffer(0, 4))
    bittree:add(f.bit1_b, buffer(0, 4))
    bittree:add(f.bit1_g, buffer(0, 4))
    ''')
    assert compare_lua(two.get_code(4), '''
    local bittree = subtree:add(f.bit2, buffer(4, 2))
    bittree:add(f.bit2_r, buffer(4, 2))
    bittree:add(f.bit2_b, buffer(4, 2))
    bittree:add(f.bit2_g, buffer(4, 2))
    ''')


# Test RangeField
ranges = Tests()

@ranges.context
def create_range_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    diss.add_field(Field('range', 'float', 4, 0, Platform.big))
    diss.children[-1].set_range_validation(0, 10)
    diss.push_modifiers()
    yield diss.children[0]
    dissector.Protocol.protocols = {}
    del proto, diss

@ranges.test
def ranges_def(field):
    """Test that RangeField generates valid defintion code."""
    assert field
    assert compare_lua(field.get_definition(), '''
    f.range = ProtoField.float("test.range", "range")
    ''')

@ranges.test
def ranges_code(field):
    """Test that RangeField generates valid code."""
    assert compare_lua(field.get_code(0), '''
    local range_node = subtree:add(f.range, buffer(0, 4))
    local range_value = buffer(0, 4):float()
    if range_value < 0 then
    range_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0")
    end
    if range_value > 10 then
    range_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 10")
    end
    ''')


# Test Field
fields = Tests()

@fields.context
def create_field():
    """Create a Protocol instance with some fields."""
    proto, diss = dissector.Protocol.create_dissector('test')
    diss.add_field(Field('one', 'float', 4, 0, Platform.big))
    diss.add_field(Field('two', 'string', 12, 0, Platform.big))
    diss.push_modifiers()
    yield diss.children[0], diss.children[1]
    dissector.Protocol.protocols = {}
    del proto, diss

@fields.test
def fields_def(one, two):
    """Test that Field generates valid defintion code."""
    assert one and two
    assert compare_lua(one.get_definition(), '''
    f.one = ProtoField.float("test.one", "one")
    ''')
    assert compare_lua(two.get_definition(), '''
    f.two = ProtoField.string("test.two", "two")
    ''')

@fields.test
def fields_code(one, two):
    """Test that Field generates valid code."""
    assert compare_lua(one.get_code(0), 'subtree:add(f.one, buffer(0, 4))')
    assert compare_lua(two.get_code(0), 'subtree:add(f.two, buffer(0, 12))')


# Test Protocol
protos = Tests()

@protos.context
def create_protos():
    """Create a Protocol instance with some fields."""
    dissector.Protocol.protocols = {}
    conf = Config('tester')
    conf.id = [25,]
    conf.description = 'This is a test'

    rules = [Trailer(conf, {'name': 'missing', 'member': 'missing', 'size': 0}),
             Trailer(conf, {'name': 'simple', 'count': 1, 'size': 4}),
             Trailer(conf, {'name': 'bur', 'count': 3, 'size': 8}),
             Trailer(conf, {'name': 'ber', 'member': 'count'})]

    proto, diss = dissector.Protocol.create_dissector('tester', None, conf)
    diss.add_field(Field('one', 'float', 4, 0, Platform.big))
    diss.add_field(Field('range', 'float', 4, 0, Platform.big))
    diss.children[-1].set_range_validation(0, 10)
    field = Field('array', 'float', 4, 0, Platform.big)
    diss.add_field(ArrayField.create([1, 2, 3], field))
    field = Field('str', 'string', 30, 0, Platform.big)
    diss.add_field(ArrayField.create([2], field))
    diss.add_field(Field('count', 'int32', 4, 0, Platform.big))
    diss.push_modifiers()
    yield proto
    dissector.Protocol.protocols = {}
    del proto, diss

@protos.test
def protos_id(proto):
    """Test that Protocol has id, description and var members."""
    assert proto
    assert proto.id == [25]
    assert proto.description.startswith('This is a test')
    assert proto.var == 'proto_tester'
    assert isinstance(list(proto.dissectors.values())[0], dissector.Dissector)
    assert isinstance(list(proto.dissectors.values())[0].children[0], Field)

@protos.test
def protos_trailer(proto):
    """Test that the Protocol has trailers."""
    assert proto.conf
    assert proto.conf.trailers
    assert len(proto.conf.trailers) == 4
    assert proto.conf.trailers[2].name == 'bur'
    assert proto.conf.trailers[3].count is None

@protos.test
def protos_create_dissector(proto):
    """Test that Protocol generates valid dissector code."""
    assert proto
    assert compare_lua(proto.generate(), '''
    -- Dissector for tester: This is a test
    local proto_tester = Proto("tester", "This is a test")
    -- ProtoField defintions for: tester
    local f = proto_tester.fields
    f.one = ProtoField.float("tester.one", "one")
    f.range = ProtoField.float("tester.range", "range")
    f.array = ProtoField.bytes("tester.array", "array")
    f.array_0 = ProtoField.bytes("tester.array.0", "array[0]")
    f.array_0_0 = ProtoField.bytes("tester.array.0.0", "array[0][0]")
    f.array_0_0_0 = ProtoField.float("tester.array.0.0.0", "array[0][0][0]")
    f.array_0_0_1 = ProtoField.float("tester.array.0.0.1", "array[0][0][1]")
    f.array_0_0_2 = ProtoField.float("tester.array.0.0.2", "array[0][0][2]")
    f.array_0_1 = ProtoField.bytes("tester.array.0.1", "array[0][1]")
    f.array_0_1_0 = ProtoField.float("tester.array.0.1.0", "array[0][1][0]")
    f.array_0_1_1 = ProtoField.float("tester.array.0.1.1", "array[0][1][1]")
    f.array_0_1_2 = ProtoField.float("tester.array.0.1.2", "array[0][1][2]")
    f.str = ProtoField.string("tester.str", "str")
    f.str_0 = ProtoField.string("tester.str.0", "str[0]")
    f.str_1 = ProtoField.string("tester.str.1", "str[1]")
    f.count = ProtoField.int32("tester.count", "count")
    -- Dissector function for: tester
    function proto_tester.dissector(buffer, pinfo, tree)
    local flag = tonumber(pinfo.private.platform_flag)
    local subtree = tree:add(proto_tester, buffer())
    if pinfo.private.field_name then
    subtree:set_text(pinfo.private.field_name .. ": tester")
    pinfo.private.field_name = nil
    else
    pinfo.cols.info:append("(This is a test)")
    end
    subtree:add(f.one, buffer(0, 4))
    local range_node = subtree:add(f.range, buffer(4, 4))
    local range_value = buffer(4, 4):float()
    if range_value < 0 then
    range_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0")
    end
    if range_value > 10 then
    range_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 10")
    end
    local array = subtree:add(f.array, buffer(8, 24))
    array:set_text("array (6 x float)")
    local subarray = array:add(f.array_0, buffer(8, 24))
    subarray:set_text("array[0] (6 x float)")
    local subsubarray = subarray:add(f.array_0_0, buffer(8, 12))
    subsubarray:set_text("array[0][0] (3 x float)")
    subsubarray:add(f.array_0_0_0, buffer(8, 4))
    subsubarray:add(f.array_0_0_1, buffer(12, 4))
    subsubarray:add(f.array_0_0_2, buffer(16, 4))
    local subsubarray = subarray:add(f.array_0_1, buffer(20, 12))
    subsubarray:set_text("array[0][1] (3 x float)")
    subsubarray:add(f.array_0_1_0, buffer(20, 4))
    subsubarray:add(f.array_0_1_1, buffer(24, 4))
    subsubarray:add(f.array_0_1_2, buffer(28, 4))
    local array = subtree:add(f.str, buffer(32, 60))
    array:add(f.str_0, buffer(32, 30))
    array:add(f.str_1, buffer(62, 30))
    subtree:add(f.count, buffer(92, 4))
    -- Trailers handling for struct: tester
    local trail_offset = 96
    local trailer = Dissector.get("simple")
    trailer:call(buffer(trail_offset, 4):tvb(), pinfo, tree)
    trail_offset = trail_offset + 4
    for i = 1, 3 do
    local trailer = Dissector.get("bur")
    trailer:call(buffer(trail_offset, 8):tvb(), pinfo, tree)
    trail_offset = trail_offset + 8
    end
    local trail_count = buffer(92, 4):int()
    for i = 1, trail_count do
    local trailer = Dissector.get("ber")
    trailer:call(buffer(trail_offset):tvb(), pinfo, tree)
    end
    end
    delegator_register_proto(proto_tester, "tester", 25, {[0]=96})
    ''')


# Test Delegator
delegator = Tests()

@delegator.context
def create_delegator():
    """Create a Protocol instance with some fields."""
    platforms = {p.name: p for flag, p in Platform.mappings.items()}
    delegator = dissector.Delegator(platforms)
    yield delegator
    del delegator

@delegator.test
def delegator_members(delegator):
    assert delegator
    assert delegator.name == 'luastructs'
    assert len(delegator.children) == 4
    assert delegator.endian == Platform.big

@delegator.test
def delegator_generate(delegator):
    assert delegator
    assert compare_lua(delegator.generate(), '''
    -- Delegator for luastructs dissectors
    local dissector_table = DissectorTable.new("luastructs", "Lua Structs", ftypes.STRING)
    local delegator = Proto("luastructs", "Lua C Structs")
    local message_ids = {}
    local dissector_sizes = {}
    -- ProtoField defintions for: luastructs
    local f = delegator.fields
    f.version = ProtoField.uint8("luastructs.Version", "Version")
    local flags_valuestring = {[0]="default", [1]="Win32", [2]="Win64", [3]="Solaris-x86", [4]="Solaris-x86-64", [5]="Solaris-sparc", [6]="Macos", [7]="Linux-x86"}
    f.flags = ProtoField.uint8("luastructs.Flags", "Flags", nil, flags_valuestring)
    f.message = ProtoField.uint16("luastructs.Message", "Message")
    f.messagelength = ProtoField.uint32("luastructs.Message_length", "Message length")
    -- Register struct dissectors
    function delegator_register_proto(proto, name, id, sizes)
    dissector_table:add(name, proto)
    if id ~= nil then message_ids[id] = name end
    if sizes ~= nil then
    for flag, size in pairs(sizes) do
    if dissector_sizes[flag] == nil then
    dissector_sizes[flag] = {}
    end
    if dissector_sizes[flag][size] == nil then
    dissector_sizes[flag][size] = {}
    end
    table.insert(dissector_sizes[flag][size], name)
    end
    end
    end
    -- Delegator dissector function for luastructs
    function delegator.dissector(buffer, pinfo, tree)
    local subtree = tree:add(delegator, buffer())
    pinfo.cols.protocol = delegator.name
    pinfo.cols.info = delegator.description
    subtree:add(f.version, buffer(0, 1))
    local flags_node = subtree:add(f.flags, buffer(1, 1))
    local flags_value = buffer(1, 1):uint()
    if flags_valuestring[flags_value] == nil then
    flags_node:add_expert_info(PI_MALFORMED, PI_WARN, "Should be in [0, 1, 2, 3, 4, 5, 6, 7]")
    end
    pinfo.private.platform_flag = flags_value
    local msg_node = subtree:add(f.message, buffer(2, 2))
    subtree:add(f.messagelength, buffer(4):len()):set_generated()
    local id_value = buffer(2, 2):uint()
    local length_value = buffer(4, 4):uint()
    -- Call the correct dissector, or try and guess which
    if message_ids[id_value] then
    msg_node:append_text(" (" .. message_ids[id_value] ..")")
    dissector_table:try(message_ids[id_value], buffer(4):tvb(), pinfo, tree)
    else
    msg_node:add_expert_info(PI_MALFORMED, PI_WARN, "Unknown message id")
    if dissector_sizes[flags_value] and dissector_sizes[flags_value][length_value] then
    for key, value in pairs(dissector_sizes[flags_value][length_value]) do
    dissector_table:try(value, buffer(4):tvb(), pinfo, tree)
    end
    end
    end
    end
    ''')

