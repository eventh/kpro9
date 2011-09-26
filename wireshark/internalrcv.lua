--
--  A sample dissector for testing Lua C structs scripts
--  Copyright 2011, Stig Bjorlykke <stig@bjorlykke.org>
-- 
-- #define INTERNALRCV 2
-- #define STRING_LEN 26
-- struct internal_rcv {
--    int    type;
--    time_t time;
--    char   data[STRING_LEN];
-- };
-- 

local PROTOCOL = Proto ("internal_rcv", "struct internal_rcv")
local luastructs_dt = DissectorTable.get ("luastructs.message")

local types = { [0] = "None", [1] = "Regular", [42] = "Secure" }

local f = PROTOCOL.fields
f.type = ProtoField.uint32 ("internal_rcv.type", "type", nil, types)
f.time = ProtoField.absolute_time ("internal_rcv.time", "time")
f.data = ProtoField.bytes ("internal_rcv.data", "data")

function PROTOCOL.dissector (buffer, pinfo, tree)
   local subtree = tree:add (PROTOCOL, buffer())
   pinfo.cols.info:append (" (" .. PROTOCOL.description .. ")")

   subtree:add (f.type, buffer(0,4))
   subtree:add (f.time, buffer(4,4))
   subtree:add (f.data, buffer(8))
end

luastructs_dt:add (2, PROTOCOL)

