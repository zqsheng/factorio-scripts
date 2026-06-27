local mod =  require('test/Signal')
local log = require('test/log')

local function assert(condition, message)
    if condition then return end
    log.ERROR('[test] ' .. message)
    
end

local function test_Clone()
    local a = {name = 'abc', value = 1}
    local t = mod.Clone(a)
    assert(a == t, "mesage")
    assert(a.name == t.name, "clone error")
    assert(a.value == t.value, "clone error.")
    
end

local function test_TypeEquals()
    local a = {name = 'abc', value = 1}
    local b = {name = 'ab', value = 1}
    assert(mod.TypeEquals(a, b), 'TypeEquals assert failed.')
end

local function test_ID()
    local a = {name = 'abc', value = 1}
    local b = {name = 'ab', value = 1}
    assert(mod.ID(a) == 0, 'ID Read failed.')
    assert(mod.ID(b) == 1, 'ID Read failed.')
    assert(mod.ID(a) == 0, 'ID Read failed.')
end

test_ID()
local a = nil

print(tostring(a))




-- test_clone()
-- test_TypeEquals()



