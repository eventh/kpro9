local PROTOCOL = Proto ("internal_snd", "struct internal_snd")
local luastructs_dt = DissectorTable.get ("luastructs.message")

local types = { [0] = "None", [1] = "Regular", [42] = "Secure" }

local f = PROTOCOL.fields
f.type = ProtoField.uint32 ("internal_snd.type", "type", nil, types)
f.time = ProtoField.absolute_time ("internal_snd.time", "time")
f.name = ProtoField.string ("internal_snd.name", "name")

function PROTOCOL.dissector (buffer, pinfo, tree)
   local subtree = tree:add (PROTOCOL, buffer())
   pinfo.cols.info:append (" (" .. PROTOCOL.description .. ")")

   subtree:add (f.type, buffer(0,4))
   subtree:add (f.name, buffer(4,30))
   subtree:add (f.time, buffer(34,4))
end

luastructs_dt:add (1, PROTOCOL)

