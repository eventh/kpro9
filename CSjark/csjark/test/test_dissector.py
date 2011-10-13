"""
Module for testing the dissector module.

Tests the output of generating dissectors.
"""
import sys, os
from attest import Tests, assert_hook, contexts

import dissector


def compare_lua(code, template):
    """Test that generated lua code equals what is expected."""
    def simplify(text):
        return ''.join(text.strip().split())
    return simplify(code) == simplify(template)


# Test EnumField
enums = Tests()

@enums.context
def create_enum_field():
    """Create a Protocol instance with some fields."""
    proto = dissector.Protocol('test', None, None)
    field = dissector.EnumField('enum', 'int32', 4, dict(enumerate('ABCDE')))
    proto.add_field(field)
    yield proto.fields[0]

@enums.test
def enum_def(field):
    assert field
    assert compare_lua(field.get_definition(), '''
f.enum = ProtoField.int32("test.enum", "enum",
    nil, {[0]="A", [1]="B", [2]="C", [3]="D", [4]="E"})
''')

@enums.test
def enum_code(field):
    """Test that EnumField generates correct code."""
    assert isinstance(field, dissector.EnumField)
    assert compare_lua(field.get_code(0), '''
local enum = subtree:add(f.enum, buffer(0, 4))
local test = {[0]="A", [1]="B", [2]="C", [3]="D", [4]="E"}
if (test[buffer(0, 4):int()] == nil) then
    enum:add_expert_info(PI_MALFORMED, PI_WARN,
    "Invalid value, not in (0, 1, 2, 3, 4)")
end
''')


# Test ArrayField
arrays = Tests()

@arrays.context
def create_array_field():
    """Create a Protocol instance with some fields."""
    proto = dissector.Protocol('test', None, None)
    proto.add_field(dissector.ArrayField('arr', 'float', 4, [1, 2, 3]))
    proto.add_field(dissector.ArrayField('str', 'string', 30, [2]))
    yield proto.fields[0], proto.fields[1]

@arrays.test
def arrays_def(one, two):
    assert one and two
    assert one.get_definition() is None

@arrays.test
def arrays_code(one, two):
    """Test that ArrayField generates correct code."""
    assert isinstance(one, dissector.ArrayField)
    assert compare_lua(one.get_code(0), '''
-- Array handling for arr
local arraytree = subtree:add("Array: arr")
local subarraytree = arraytree:add("Array: ")
local subsubarraytree = subarraytree:add("Array: ")
subsubarraytree:add(ProtoField.float("arr"), buffer(0, 4):float())
subsubarraytree:add(ProtoField.float("arr"), buffer(4, 4):float())
subsubarraytree:add(ProtoField.float("arr"), buffer(8, 4):float())
local subsubarraytree = subarraytree:add("Array: ")
subsubarraytree:add(ProtoField.float("arr"), buffer(12, 4):float())
subsubarraytree:add(ProtoField.float("arr"), buffer(16, 4):float())
subsubarraytree:add(ProtoField.float("arr"), buffer(20, 4):float())
''')

@arrays.test
def arrays_str(one, two):
    assert isinstance(two, dissector.ArrayField)
    assert compare_lua(two.get_code(0), '''
-- Array handling for str
local arraytree = subtree:add("Array: str")
arraytree:add(ProtoField.string("str"), buffer(0, 30):string())
arraytree:add(ProtoField.string("str"), buffer(30, 30):string())
''')

#Test StuctField
structs = Tests()

@structs.context
def create_struct_field():
    proto = dissector.Protocol('test', None, None)
    proto.add_field(dissector.SubDissectorField('test', 8, 32, 'testStructType'))
    proto.add_field(dissector.SubDissectorField('test2', 9, 64, 'testStructType2'))
    yield proto.fields[0], proto.fields[1]

@structs.test
def struct_def(one, two):
    assert one and two
    assert one.get_definition() is None
    assert two.get_definition() is None

@structs.test
def struct_code(one, two):
    assert isinstance(one, dissector.SubDissectorField)
    assert isinstance(two, dissector.SubDissectorField)
    assert compare_lua(one.get_code(0), '''
    local subsubtree = subtree:add("test:")
    luastructs_dt:try(8, buffer(0, 32):tvb(), pinfo, subsubtree)
    ''')
    assert compare_lua(two.get_code(32), '''
    local subsubtree = subtree:add("test2:")
    luastructs_dt:try(9, buffer(32, 64):tvb(), pinfo, subsubtree)
    ''')