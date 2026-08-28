# Factorio API Skill

Use this skill when a request asks about Factorio Lua scripting APIs, events,
prototypes, entities, surfaces, forces, inventories, signals, or mod settings.

- Ask for the Factorio version when the request does not specify one. Treat 1.1
  and 2.0 APIs as potentially different.
- Prefer the official versioned Lua API reference at
  `https://lua-api.factorio.com/`; use the matching version rather than
  assuming `latest` applies.
- Inspect this repository with `search_factorio_files` before making claims
  about local wrappers, event names, prototypes, or existing conventions.
- When documentation is unavailable, say so and distinguish documented API
  behavior from an educated guess. Do not invent method names or fields.
- Provide concise Lua examples with the relevant event or lifecycle context,
  and mention whether code belongs in `data.lua`, `control.lua`, or another
  mod stage.
- Check for nil values, invalid entity state, multiplayer surfaces and forces,
  and event lifecycle issues in examples where they matter.
- Do not claim an API example was tested in-game unless it was actually tested
  against the requested Factorio version.
