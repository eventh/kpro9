---
-- Created by IntelliJ IDEA.
-- User: sigurd
-- Date: 22.09.11
-- Time: 19:09
-- To change this template use File | Settings | File Templates.
--

print("Hello world!")

Type = {_typename  = "", _default_size = 0, _default_endiam = ""}

function Type:new (typeName, defualt_size, default_endian)
  o = {_typeName = typeName, _defualt_size = defualt_size, _default_endian = default_endian}
  setmetatable(o, self)
  self.__index = self
  return o
end

function Type:add(flag, size, endian) end

function Type:getSize(flag)
  return self._defualt_size
end

int = Type:new("int", 4, "big")

int:add(1, 4, "big")

print(int)

print(int:getSize(""))