local proto_age_test = Proto("age_test", "a struct with an age in it!")
local luastructs_dt = DissectorTable.get("luastructs.message")

local f = proto_age_test.fields
f.name = ProtoField.string("age_test.name", "name")
f.age = ProtoField.int32("age_test.age", "age")

function proto_age_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_age_test, buffer())
	pinfo.cols.info:append(" (" .. proto_age_test.description .. ")")

	subtree:add(f.name, buffer(0, 10))
	local age = subtree:add(f.age, buffer(10, 4))
	local age_val = buffer(10, 4):int()
	if (0.0 > age_val) then
		age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
	end
	local age_val = buffer(10, 4):int()
	if (100.0 < age_val) then
		age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 100.0")
	end
end

luastructs_dt:add(9, proto_age_test)
