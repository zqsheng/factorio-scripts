# Google OR-Tools Skill

Use this skill when a request involves Google OR-Tools, constraint programming,
integer optimization, routing, scheduling, path planning, or factory layout.

- Prefer `RoutingModel` for multi-stop routing and `CpModel`/`CpSolver` for
  discrete placement, scheduling, collision, and resource constraints.
- Use `Assignment` or min-cost flow when the problem is primarily matching or
  capacity allocation.
- For Factorio layouts, model machine positions, belt paths, non-overlap,
  throughput, power, and construction cost as explicit variables and constraints.
- Define the objective clearly, such as shortest total belt length, fewest turns,
  maximum throughput, minimum cost, or a weighted combination.
- Keep the existing A\* grid search for a quick single source-to-target path when
  global optimization is unnecessary; use OR-Tools when routes interact.
- Do not claim an optimization result is globally optimal unless the solver proves
  optimality. Report time limits and solver status.
- Validate coordinates, footprints, capacities, and Factorio version-dependent
  entities before generating a blueprint.

When the repository already provides a layout optimizer, prefer adding an OR-Tools
model around its existing domain objects rather than duplicating grid and metric
definitions.
