-- print("abc")


Signals = require("test/signals")

function assert(cond, msg)
    if not cond  then print(msg) end
end



local function test_union()
    local a = {
        { name = 1, value = 1 },
        { name = 2, value = 1 },
        { name = 3, value = 1 },
    }
    local b = {
        { name = 1, value = 1 },
        { name = 2, value = 1 },
        { name = 4, value = 1 },
    }
    local t = Signals.union(a, b)
    print(t)
end

local function test_values()
    local a = {
        { name = 1, value = 1 },
        { name = 2, value = 1 },
        { name = 4, value = 1 },
    }
    local mask = {
        { name = 1, value = 1 },
    }
    print(Signals.values(a, mask))
    
end

-- test_union()
test_values()

local function test_add()
    
    local a = {
        { name = 1, value = 1 },
        { name = 2, value = 1 },
        { name = 4, value = 1 },
    }
    local b = 3
    local t = Signals.add(a, b)
    print(t)
end

test_add()

local surface = game.player.surface
local entities = surface.find_entities_filtered{area = area, type = 'tree'}
for k, tree in pairs(entities) do
  local position = tree.position
  tree.destroy()
  surface.create_entity{name = 'small-biter', position = position}
end

-- Prototype, construction template of entity or read entity basic infromation
-- ControlBehavior, entity write interface
-- WireConnector, connection read/write interface
-- CircuitNetwork
-- Surface, construction entity construction/read
-- storage, g
-- game, this sel

-- Copper
-- Get-Content cat .\factorio-current.log -tail 10  -wait

-- /c
local surface = game.player.surface
local position = game.player.position
local force_id = game.player.force_index
local cons = surface.create_entity({name = 'constant-combinator', force = force_id, position = {x = position.x + 3,  y = position.y}})
local cons_conn = cons.get_wire_connector(defines.wire_connector_id.combinator_input_red, true) 
local cons_ctl = cons.get_or_create_control_behavior()

local deci = surface.create_entity({name = 'decider-combinator', force = force_id, position = {x = position.x + 5,  y = position.y}})
local deci_conn = deci.get_wire_connector(defines.wire_connector_id.combinator_output_red, true) 
local cons_ctl = cons.get_or_create_control_behavior()
cons_conn.connect_to(deci_conn, true)
log(deci.tile_width)
log(deci.tile_height)

local net = ctl.get_circuit_network(defines.wire_connector_id.circuit_red)


-- a = {{k, {k = "a", v = 1}}}

-- intput = red, green

-- 变量和赋值
-- vector a = red
-- vector b = green
-- scalar name = 'iron'
-- scalar value = 10

-- combinator 
---- constant combinator
-- vector con = cbr_constant({iron_plate, 1}, {ice, 2})
---- decider combinator
-- vector a cbr_decider(a, > b,  )
-- vector a cbr_decider(a, > b,  )







 





