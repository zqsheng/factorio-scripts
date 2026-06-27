
-- defines 

local mod = {}


local context = {
    tick = 0,
    r_in = {},
    g_in = {}, 
    prev = {},
    next = {},
}

-- everything

function mod.Each(a, b, op)
    
    
end

function mod.Anything(a, b, op)
    
end

function mod.Select(r, g, mask) 
    if mask == 0 then return nil end
    if mask == 1 then return r end
    if mask == 2 then return g end
    return mod.Union(r, g)
end


-- priority and > or 


local Parameter = {
    value = {}, 
    type = 0
}


mod.ParamterType_Numerical = 1
mod.ParamterType_Vector = 2


function mod.Everything(ctx, a, b, arch) 
    if ctx.red_in or ctx.green_in  then  return true end -- todo
    if a.type == mod.ParamterType_Numerical and b.type == mod.ParamterType_Numerical then return arch(a.value, b.value) end

    if a.type == mod.ParamterType_Numerical and b.type == mod.ParamterType_Vector then 
        for _, x in pairs(b) do 
            if not arch(a.value, x.value)  then return false end
        end
    end
    if a.type == mod.ParamterType_Vector and b.type == mod.ParamterType_Numerical then 
        for _, x in pairs(a) do 
            if not arch(x.value, b.value)  then return false end
        end
    end
    return false
end


local NotCalause  = {
    first = 0, second = 0,
    apply = function ()
        return ~first
    end
}

local OrCaluse = {
    first = 0, second = 0,
     apply = function ()
        return first or second
     end
}
local AndCaluse = {
    first = 0, second = 0,
    apply = function ()
        return first and second
     end
}



-- append()
local a, b, c = true, false, false
print(a and b or c)




local Proposition = {
    ctx = {},
    Caluse = {},
    apply = function (ctx)
        
    end
}


local DeciderCombinator = {
    red = {}, green = {}, 
    proposition = {},
    outputSelect = {}
}



-- prev

-- select 1, select 2


-- prev

-- post