
local sl = require('test/signal')
local util = {}
local mod = util

function mod.CreateSignal()
    return {name = math.random(100), value = math.random(1000, 10000)}
end

function mod.CreateVector(n)
    local list = {}
    if not n then n = 20 end
    local mask = 0
    for i = 1, n do 
        local a = mod.CreateSignal()
        local id = sl.ID(a)
        table.insert(list, a)
        mask = mask | 1 << id
    end
    return {signals = list, mask = mask}
end


return mod