local proto_cenum_test = Proto("cenum_test", "a struct with an enum in it!")
local luastructs_dt = DissectorTable.get("luastructs.message")

local f = proto_cenum_test.fields
f.id = ProtoField.int32("cenum_test.id", "id")
f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, {[1]="FEB", [2]="MAR", [3]="APR", [4]="MAY", [5]="JUN", [6]="JUL", [7]="AUG", [8]="SEP", [9]="OCT", [10]="NOV", [20]="DEC"})

function proto_cenum_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_cenum_test, buffer())
	pinfo.cols.info:append(" (" .. proto_cenum_test.description .. ")")

	subtree:add(f.id, buffer(0, 4))
	local mnd = subtree:add(f.mnd, buffer(4, 4))
	local test = {[1]="FEB", [2]="MAR", [3]="APR", [4]="MAY", [5]="JUN", [6]="JUL", [7]="AUG", [8]="SEP", [9]="OCT", [10]="NOV", [20]="DEC"}
	if (test[buffer(4, 4):uint()] == nil) then
		mnd:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20)")
	end
end

luastructs_dt:add(11, proto_cenum_test)
