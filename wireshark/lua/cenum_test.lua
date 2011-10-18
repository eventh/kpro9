-- Dissector for struct: cenum_test: C Enum test
local proto_cenum_test = Proto("cenum_test", "C Enum test")
local luastructs_dt = DissectorTable.get("luastructs.message")

-- ProtoField defintions for struct: cenum_test
local f = proto_cenum_test.fields
f.id = ProtoField.int32("cenum_test.id", "id")
f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"})

-- Dissector function for struct: cenum_test
function proto_cenum_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_cenum_test, buffer())
        if pinfo.private.structname then
	   subtree:set_text (pinfo.private.structname)
        end
	pinfo.cols.info:append(" (" .. proto_cenum_test.description .. ")")

	subtree:add(f.id, buffer(0, 4))
	local mnd = subtree:add(f.mnd, buffer(4, 4))
	local test = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"}
	if (test[buffer(4, 4):uint()] == nil) then
		mnd:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20)")
	end
end

luastructs_dt:add(11, proto_cenum_test)
