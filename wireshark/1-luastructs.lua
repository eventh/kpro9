--
--  A sample dissector for testing Lua C structs scripts
--  Copyright 2011, Stig Bjorlykke <stig@bjorlykke.org>
--

local LUASTRUCTS = Proto ("luastructs", "Lua C Structs")
local luastructs_dt = DissectorTable.new ("luastructs.message", "LUASTRUCTS")

local f = LUASTRUCTS.fields
f.version = ProtoField.uint8 ("luastructs.version", "Version")
f.flags   = ProtoField.uint8 ("luastructs.flags", "Flags")
f.message = ProtoField.uint16 ("luastructs.message", "Message")
f.length  = ProtoField.uint32 ("luastructs.length", "Message length")

function LUASTRUCTS.dissector (buffer, pinfo, tree)
   local subtree = tree:add (LUASTRUCTS, buffer())
   pinfo.cols.protocol = LUASTRUCTS.name
   pinfo.cols.info = LUASTRUCTS.description

   subtree:add (f.version, buffer(0,1))
   flags = buffer(1,1):uint()              -- Make this global for subdissectors
   subtree:add (f.flags, buffer(1,1))

   local message = buffer(2,2):uint()
   local mi = subtree:add (f.message, buffer(2,2))
   mi:append_text (" (" .. tostring (luastructs_dt:get_dissector (message)) .. ")")

   subtree:add (f.length, buffer(4):len()):set_generated()
   luastructs_dt:try (message, buffer(4):tvb(), pinfo, tree)
end
