---
-- Created by IntelliJ IDEA.
-- User: sigurd
-- Date: 22.09.11
-- Time: 19:09
-- To change this template use File | Settings | File Templates.
--

Type = {_typename  = "", _default_size = 0, _default_endiam = "", _flag_configs = {}}

function Type:new (typeName, defualt_size, default_endian)
  o = {_typeName = typeName, _defualt_size = defualt_size, _default_endian = default_endian, flag_configs = {}}
  setmetatable(o, self)
  self.__index = self
  return o
end

function Type:add(flag, size, endian)
  self._flag_configs[flag] = {_size = size, _endian = endian}
end

function Type:getSize(flag)
  local flag_config = self._flag_configs[flag]

  if not (flag_config == nil) then
    return flag_config._size
  end

  return self._defualt_size
end

types = {}

types["int"] = Type:new("int", 4, "big")

types["char"] = Type:new("char", 4, nil)

types["long"] = Type:new("long", 8, "little")

print(int:getSize(1))

int:add(1, 8, "big")

print(int:getSize(1))