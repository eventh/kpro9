local proto_age_test = Proto("age_test", "struct age_test")
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
	local age_min = 0.0
	if (age_min > age_val) then
		age:append_text(" INVALID")
	end
	local age_val = buffer(10, 4):int()
	local age_max = 100.0
	if (age_max < age_val) then
		age:append_text(" INVALID")
	end
end

luastructs_dt:add(9, proto_age_test)
