---
-- Created by IntelliJ IDEA.
-- User: sigurd
-- Date: 22.09.11
-- Time: 19:09
-- To change this template use File | Settings | File Templates.
--

function Type:new(o)
  o = o or {}
  setmetatable(o, self)
  self.__intex = self
end

function Type:add(a) end
