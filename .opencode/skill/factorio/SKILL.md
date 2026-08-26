---
name: factorio
description: Use when generating Factorio blueprints. Trigger on "blueprint", "factorio blueprint", "generate blueprint", or requests to build/layout Factorio factories, belts, or entities as blueprint JSON.
---

# Factorio Blueprint Skill

Helps generate Factorio blueprints as importable blueprint strings.

## Blueprint format

A Factorio blueprint is JSON with this top-level shape:

```json
{
  "blueprint": {
    "icons": [{"signal": {"type": "item", "name": "assembling-machine-1"}, "index": 1}],
    "entities": [ ... ],
    "item": "blueprint"
  }
}
```

Each entity inside `entities` needs at least:

```json
{
  "entity_number": 1,
  "name": "assembling-machine-1",
  "position": {"x": 0.5, "y": 0.5},
  "direction": 0
}
```

- `entity_number` — unique 1-based integer, sequential.
- `name` — exact in-game prototype name (e.g. `transport-belt`, `inserter`,
  `electric-furnace`, `assembling-machine-2`).
- `position` — center of the entity; many entities sit on half-tile offsets.
- `direction` — 0, 2, 4, 6 (up, right, down, left). Belts/inserters/machines
  matter; default 0.

Optional common fields: `recipe`, `items` (modules), `request_filters`,
`connections` (circuit/red-green wires), `control_behavior`.

## Making it importable (blueprint string)

A blueprint string = `0` byte + zlib-deflate(JSON) + base64, prefixed with
`0` version byte. Encode/decode with Python:

```python
import base64, zlib, json

def encode(blueprint_json: dict) -> str:
    raw = json.dumps(blueprint_json).encode()
    return "0" + base64.b64encode(zlib.compress(raw)).decode()

def decode(string: str) -> dict:
    return json.loads(zlib.decompress(base64.b64decode(string[1:])))
```

The importable code is `"0" + encode({...})` (the string already includes the
version `0` prefix). Paste the result directly into Factorio's blueprint paste
field.

## Workflow

1. Decide entities + a tile grid (leave room on half-tile centers).
2. Build the `entities` list with sequential `entity_number`.
3. Add `icons` for a recognizable toolbar icon.
4. Encode to a blueprint string and hand it back to the user.
5. Offer a decode round-trip to verify validity.

## Tips

- Keep belts aligned to a grid; mismatched half-tile offsets break connections.
- For long belts, chain positions carefully; direction controls flow.
- Use `connections` only when the user wants circuit or logistic wiring.
