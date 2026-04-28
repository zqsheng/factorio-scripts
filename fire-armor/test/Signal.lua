 local mod_signal = {}
 local mod = mod_signal

MaskDict = {}
MaskCounter = 0
 


 -- Signal Define
 local Signal = {name  = '', value = 0}
 
 todo
 local 

 
    
 function mod.Clone(s)
    return {name = s.name, value = s.value}
end

function mod.TypeEquals(a, b)
    if not a and not b then return true end
    if a.name == b.name  then return true end
    return false
end

function mod.Equals(a, b)
    if not a and not b then return true end
    if a.name == b.name  and a.value == b.value then return true end
    return false
end

function  mod.ID(k)
    local id = MaskDict[k.name]
    if id then return id end
    MaskDict[k.name] = MaskCounter
    MaskCounter = MaskCounter + 1
    return MaskCounter - 1
end

function mod.Pretty(x)
    return string.format("signal{name =%d, value =%d}",  x.name, x.value)
    
end
return mod
