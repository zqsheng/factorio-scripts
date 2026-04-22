

local mod = {}

local InRed = 1
local InGreen = 2
local OutRed = 4
local OutGreen = 8

local function TrueIfNil(x)
    if not x then return  true end
    return x
end
function ConstantCombinator(ctx, enabled, items) 
    local forceID = ctx.forceID
    local position = ctx.position
    local comb = ctx.surface.create_entity({name = 'constant-combinator', force = forceID, position = {x = position.x + 1,  y = position.y}})
    local ctl = comb.get_or_create_control_behavior()
    local combinator = {combinator = comb, connectors = {}}
    combinator.connectors[OutRed] = comb.get_wire_connector(defines.wire_connector_id.circuit_red, true) 
    combinator.connectors[OutGreen] = comb.get_wire_connector(defines.wire_connector_id.circuit_green, true) 
    
    ctl.enabled = TrueIfNil(enabled)
    if items and #items > 0 then 
        local filters = {}
        for _, x in pairs(items) do 
            local t  = {value = x.item, min = x.count, max = x.count}
            table.insert(filters, t)
        end
        local section = table.deepcopy(data.raw['logistic-section'])
        log(tostring(section))
        
        local filter = {}
        
        local section  = {}
    end
    
    
    return combinator
end
function DeciderCombinator(ctx, available, items) 
    local forceID = ctx.forceID
    local position = ctx.position
    local comb = ctx.surface.create_entity({name = 'decider-combinator', force = forceID, position = {x = position.x + 2,  y = position.y}})
    local combinator = {combinator = comb, connectors = {}}
    combinator.connectors[InRed] = comb.get_wire_connector(defines.wire_connector_id.combinator_input_red, true) 
    combinator.connectors[InGreen] = comb.get_wire_connector(defines.wire_connector_id.combinator_input_green, true) 
    combinator.connectors[OutRed] = comb.get_wire_connector(defines.wire_connector_id.combinator_output_red, true) 
    combinator.connectors[OutGreen] = comb.get_wire_connector(defines.wire_connector_id.combinator_output_green, true) 
    return combinator
end

function mod.Wire(a, a_solt, b, b_solt)
    a.connectors[a_solt].connect_to(b.connectors[b_solt])
end

function  mod.Append(tb, x)  
    table.insert(tb, {item = x.item, value = x.count})
end


function mod.BuildContext(event) 
    local ctx = {
        
    }
    local player = game.get_player(event.player_index)
    local surface = player.surface
    local position = player.position
    local chunk = event.parameters
    local forceID = player.force_index
    ctx.forceID = forceID
    ctx.surface = surface
    ctx.position = position
    ctx.InRed = InRed
    ctx.OutRed = OutRed
    ctx.InGreen = InGreen
    ctx.OutGreen = OutGreen
    ctx.ConstantCombinator = function (available, items)
        return ConstantCombinator(ctx, available, items)
    end
    ctx.DeciderCombinator = function (available, items)
        return DeciderCombinator(ctx, available, items)
    end
    ctx.Wire = function (a, a_solt, b, b_solt)
        mod.Wire(a, a_solt, b, b_solt)
    end
    ctx.Append = mod.Append
    local cmd = assert(load(chunk,'user_command','t', ctx), "syntax error.")
    if not cmd  then 
        assert("code isn't is nil")
    end
   ctx['command'] = cmd
   return ctx
end





function mod.Construction(ctx)
    ctx.command()
end
return mod
