-- Dissector for win32.temperature: temperature (Win32)
local proto_temperature = Proto("win32.temperature", "temperature (Win32)")

-- ProtoField defintions for: temperature
local f = proto_temperature.fields
f.celsius = ProtoField.int32("temperature.celsius", "celsius")
-- This is below 'celsius'

-- Dissector function for: temperature
function proto_temperature.dissector(buffer, pinfo, tree)
	local subtree = tree:add_le(proto_temperature, buffer())
	if pinfo.private.caller_def_name then
		subtree:set_text(pinfo.private.caller_def_name .. ": " .. proto_temperature.description)
		pinfo.private.caller_def_name = nil
	else
		pinfo.cols.info:append(" (" .. proto_temperature.description .. ")")
	end

	-- This is above 'celsius' inside the dissector function.
	subtree:add_le(f.celsius, buffer(0, 4))
	-- This is below 'celsius' inside dissector function
end

delegator_register_proto(proto_temperature, "Win32", "temperature", 7004)
