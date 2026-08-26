import base64, zlib, json

def encode(bp):
    raw = json.dumps(bp).encode()
    return "0" + base64.b64encode(zlib.compress(raw)).decode()

recipes = [
    ("copper-cable",        [("copper-plate", 50)]),
    ("iron-gear-wheel",     [("iron-plate", 100)]),
    ("pipe",                [("iron-plate", 100)]),
    ("iron-stick",          [("iron-plate", 100)]),
    ("electronic-circuit",  [("iron-plate", 50), ("copper-cable", 100)]),
    ("inserter",            [("electronic-circuit", 50), ("iron-gear-wheel", 50)]),
]

entities = []
n = 0
def add(name, x, y, **kw):
    global n
    n += 1
    e = {"entity_number": n, "name": name,
         "position": {"x": float(x), "y": float(y)}}
    e.update(kw)
    entities.append(e)
    return e

for i, (recipe, reqs) in enumerate(recipes):
    mx = i * 7 + 0.5      # assembler center x
    my = 0.5
    # requester chest (left)
    add("logistic-chest-requester", mx - 3, my,
        request_filters=[{"name": r, "count": c, "index": idx+1}
                          for idx, (r, c) in enumerate(reqs)])
    # input inserter
    add("fast-inserter", mx - 2, my, direction=2)
    # assembler
    add("assembling-machine-3", mx, my, direction=0, recipe=recipe)
    # output inserter
    add("fast-inserter", mx + 2, my, direction=2)
    # passive provider chest (right)
    add("logistic-chest-passive-provider", mx + 3, my)
    # power pole above the module
    add("medium-electric-pole", mx, my + 3)

# central roboport (within pole supply, covers whole mall)
add("roboport", 17.5, 9.5)

bp = {
    "blueprint": {
        "icons": [
            {"signal": {"type": "item", "name": "assembling-machine-3"}, "index": 1},
            {"signal": {"type": "item", "name": "logistic-chest-passive-provider"}, "index": 2},
        ],
        "entities": entities,
        "item": "blueprint",
    }
}

print(encode(bp))
print("entity_count:", len(entities), file=__import__("sys").stderr)
