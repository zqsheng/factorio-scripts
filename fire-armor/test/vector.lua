
local signal = require('test/signal')

local Vector = {signals = {}, mask = 0}
local mod = Vector

function mod.Clone(vt) 
    if not vt then return nil end
    local sl = {}
    for _, x in pairs(vt.signals) do 
        table.insert(sl, signal.Clone(x))
    end
    return {signals = sl, mask = vt.mask}
end

-- todo support neg number
function mod.Append(v, x) 
    if v then return nil end --todo
    local id = signal.ID(x)
    if v.mask >> id & 1 then 
        v[x] = v[x] + x.value
        return
    end
    table.insert(v.signal, x)
    v.mask = v.mask | 1 << id
end

-- todo support neg number
function mod.Union(s, t)
    if not s and not t then return nil end
    if not s then return mod.Clone(t) end
    if not t then return mod.Clone(s) end
    local sCloned = mod.Clone(s)
    for _, x in pairs(t.signals) do
        mod.Append(sCloned, x)
    end
    return s.sCloned
end

function mod.Complement(s)
    local t = signal.MaskCounter - 1
    return t ~ s.mask
end


-- todo support neg number
function mod.Interaction(s, t) 
    if not s or not t or s.mask & t.mask == 0 then return nil end
    local sl = {}
    local mask = s.mask & t.mask
    for _, x in pairs(s) do
        if 1 << signal.ID(x) & mask > 0 then 
            table.insert(sl, signal.Clone(x))
        end
    end
    local int = {signals = sl, mask = mask}
    for _, x in pairs(s) do
        if 1 << signal.ID(x) & mask > 0 then 
            mod.Append(int, x)
        end
    end
    return int
end

function mod.Selector(r, g, mask) 
    if mask == 1 then return r end
    if mask == 2 then return g end
    return mod.Union(r, g)
end

 
function mod.forall(a, b, arch)
    
end
function mod.each()
    
end
-- Predicate 
-- 

-- 集合非空
-- \forall 

function mod.Null(vt)
    
end

-- 

-- Arithmetic Operation 
-- 
-- 
-- 

function Set(v)
    return v
end
function add(a, b)
    return a + b
end
function mul(a, b)
    return a * b
end




return Vector
    
    