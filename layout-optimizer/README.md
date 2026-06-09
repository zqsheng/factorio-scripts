# Factorio Layout Optimizer

A grid-based belt routing engine and mathematical model for optimizing Factorio factory layouts.

## Overview

This package provides tools to design and optimize belt networks in Factorio by:
- Modeling belt types with different speeds and capacities
- Using A* pathfinding to route belts while avoiding obstacles
- Calculating path costs, travel times, and network metrics
- Visualizing layouts on a 2D grid

## Project Structure

```
layout-optimizer/
├── model.py          # Belt types, paths, and network models
├── grid.py           # Grid representation and A* pathfinding
├── optimizer.py      # Layout optimization engine
├── main.py           # CLI entrypoint
├── __init__.py       # Package exports
└── README.md         # This file
```

## Mathematical Model

### Belt Types

Conveyor belts have different speeds (tiles per second):

- **YELLOW**: 15 tiles/s
- **RED**: 30 tiles/s
- **BLUE**: 45 tiles/s

### Underground Belt Types

Underground belts allow transport belts to cross beneath other belts.

**Reference:** https://wiki.factorio.com/Underground_belt

| Belt Type | Speed | Cost/Unit | Max Distance |
|-----------|-------|-----------|--------------|
| Yellow | 15 items/s | 10 | 4 tiles |
| Red | 30 items/s | 20 | 4 tiles |
| Blue | 45 items/s | 30 | 4 tiles |

**Underground Belt Features:**
- Used to allow transport belts to cross underneath other belts
- Maximum underground distance: 4 squares
- Cannot transport items beneath lava (Space Age) and space void
- Speed same as corresponding belt type
- Path validation ensures distance constraints are met

### Ground Belt Types

Ground belts are infrastructure tiles that characters walk on. Different materials provide movement speed bonuses:

| Material | Speed Multiplier | Cost/Tile | Max Cross Width | Effect |
|----------|-----------------|-----------|-----------------|--------|
| Stone | 1.00x | 1 | 1 tile | Normal movement |
| Concrete | 1.15x | 5 | 2 tiles | +15% faster |
| Refined Concrete | 1.25x | 10 | 3 tiles | +25% faster |
| Hazard Concrete | 1.25x | 12 | 3 tiles | +25% faster (visual warning) |

**Ground Belt Model:**
- `speed_multiplier`: character movement speed bonus
- `cost_per_tile`: construction resources required
- `maximum_cross_tile`: width characters can cross
- `length`: number of tiles in the path
- `total_cost`: length × cost_per_tile
- `average_speed_multiplier`: weighted speed across path
- `cost_per_tile`: average cost efficiency

### BeltPath Metrics

Each routed conveyor belt path has:
- `length`: Number of tiles
- `turns`: Number of direction changes
- `travel_time`: length / belt_speed
- `capacity`: tiles/second the belt can carry
- `cost`: length + turn_penalty * turns (default penalty = 2.0)

### BeltNetwork Metrics

The complete conveyor belt network provides:
- `total_length`: Sum of all belt lengths
- `total_turns`: Sum of all direction changes
- `average_travel_time`: Mean travel time across paths
- `bottleneck_capacity`: Minimum capacity in the network
- `total_cost`: Sum of all individual path costs

### GroundBeltNetwork Metrics

The complete ground belt network provides:
- `total_length`: Sum of all ground belt tile counts
- `total_cost`: Sum of all construction costs
- `average_speed_multiplier`: Weighted average movement speed bonus
- `cost_per_tile`: Average construction cost per tile

### UndergroundBeltNetwork Metrics

The complete underground belt network provides:
- `total_length`: Sum of all underground belt lengths
- `valid_paths_count`: Number of paths respecting max distance constraint
- `total_cost`: Sum of all construction costs
- `bottleneck_capacity`: Minimum capacity in network
- `average_travel_time`: Mean travel time across paths

### Lab Types

Research facilities for scientific research progress.

**Reference:** https://wiki.factorio.com/Lab and https://wiki.factorio.com/Biolab

| Lab Type | Speed | Science Drain | Effective Speed | Power | Module Slots | Notes |
|----------|-------|----------------|-----------------|-------|--------------|-------|
| Standard | 1.0x | 100% | 1.00x | 60 kW | 2 | Base game |
| Biolab | 2.0x | 50% | 4.00x | 300 kW | 4 | Space Age only |

**Key Insights:**
- Biolab has 100% speed bonus (2x research speed)
- Biolab has 50% science drain (consumes half the packs)
- Combined: biolab gives 4x effective speed (double speed + half consumption)
- Biolab multiplies with research speed technologies
- Biolab consumes same packs as standard lab but provides double research progress

### Lab and LabCluster Metrics

Lab clusters aggregate research facilities:
- `lab_count`: Total number of labs
- `biolab_count`: Number of biolabs
- `total_cost`: Sum of all lab costs
- `total_energy_consumption_kw`: Total power requirement
- `average_speed_multiplier`: Average research speed
- `average_science_drain`: Average pack consumption rate
- `average_effective_speed`: Average efficiency (speed / drain)
- `total_module_slots`: Total available productivity/speed slots

## Usage

### Basic Example

```python
from layout_optimizer import LayoutOptimizer, BeltType

# Create a 20x12 grid with an obstacle at x=7
optimizer = LayoutOptimizer(
    width=20, 
    height=12, 
    obstacles={(7, y) for y in range(2, 10)}
)

# Add belt links
optimizer.add_link((1, 1), (18, 2), "input-1", BeltType.RED)
optimizer.add_link((1, 4), (18, 5), "input-2", BeltType.YELLOW)
optimizer.add_link((1, 8), (18, 9), "input-3", BeltType.BLUE)

# Optimize layout
network = optimizer.optimize()

# Visualize
print(optimizer.render(network))
print(network.summary())

# Inspect individual paths
for path in network.paths:
    print(path.describe())
```

### Running the Demo

```bash
python3 main.py
```

Output:
```
....................
.S*******...........
.......#**********T.
.......#............
.S.....#............
.******#**********T.
......*#*...........
......*#*...........
.S....*#*...........
.******#**********T.
.....*****..........
.....*****..........
BeltNetwork(total_length=68, total_turns=12, avg_travel_time=0.99s, bottleneck_capacity=15.0, total_cost=92.0)
BeltPath((1, 1) -> (18, 2), type=red, length=18, turns=2, travel_time=0.60s, capacity=30.0, cost=22.0)
BeltPath((1, 4) -> (18, 5), type=yellow, length=28, turns=5, travel_time=1.87s, capacity=15.0, cost=38.0)
BeltPath((1, 8) -> (18, 9), type=blue, length=22, turns=5, travel_time=0.49s, capacity=45.0, cost=32.0)
```

### Grid Visualization Legend

- `S` = source point (belt start)
- `T` = target point (belt end)
- `*` = belt path
- `#` = obstacle
- `.` = empty space

## API Reference

### LayoutOptimizer

```python
LayoutOptimizer(width, height, obstacles=None)
  .add_link(source, target, name="", belt_type=BeltType.YELLOW)
  .optimize() -> BeltNetwork
  .render(belt_network) -> str
```

### BeltPath

```python
BeltPath(source, target, path, belt_type=BeltType.YELLOW, turn_penalty=2.0)
  .length -> int
  .turns -> int
  .travel_time -> float
  .capacity -> float
  .cost -> float
  .describe() -> str
```

### BeltNetwork

```python
BeltNetwork(paths)
  .total_length -> int
  .total_turns -> int
  .average_travel_time -> float
  .bottleneck_capacity -> float
  .total_cost -> float
  .summary() -> str
```

### GroundBeltType

```python
GroundBeltType.STONE
GroundBeltType.CONCRETE
GroundBeltType.REFINED_CONCRETE
GroundBeltType.HAZARD_CONCRETE

# Properties
  .speed_multiplier -> float
  .cost_per_tile -> int
  .maximum_cross_tile -> int
```

### GroundBelt

```python
GroundBelt(position, material=GroundBeltType.STONE)
  .position -> Point
  .material -> GroundBeltType
  .cost -> int
  .speed_boost -> float
  .maximum_cross_tile -> int
  .describe() -> str
```

### GroundBeltPath

```python
GroundBeltPath(source, target, path, material=GroundBeltType.STONE)
  .length -> int
  .total_cost -> int
  .average_speed_multiplier -> float
  .maximum_cross_tile -> int
  .describe() -> str
```

### GroundBeltNetwork

```python
GroundBeltNetwork(paths)
  .total_length -> int
  .total_cost -> int
  .average_speed_multiplier -> float
  .cost_per_tile -> float
  .summary() -> str
```

### UndergroundBeltType

```python
UndergroundBeltType.YELLOW  # 15 items/s, cost 10, max distance 4
UndergroundBeltType.RED     # 30 items/s, cost 20, max distance 4
UndergroundBeltType.BLUE    # 45 items/s, cost 30, max distance 4

# Properties
  .speed -> float
  .cost_per_unit -> int
  .max_distance -> int
```

### UndergroundBelt

```python
UndergroundBelt(position, belt_type=UndergroundBeltType.YELLOW)
  .position -> Point
  .belt_type -> UndergroundBeltType
  .cost -> int
  .speed -> float
  .max_distance -> int
  .describe() -> str
```

### UndergroundBeltPath

```python
UndergroundBeltPath(source, target, path, belt_type=UndergroundBeltType.YELLOW)
  .length -> int
  .total_cost -> int
  .speed -> float
  .capacity -> float
  .travel_time -> float
  .is_valid_distance() -> bool  # Checks if length <= max_distance
  .describe() -> str
```

### UndergroundBeltNetwork

```python
UndergroundBeltNetwork(paths)
  .total_length -> int
  .total_cost -> int
  .total_capacity -> float
  .bottleneck_capacity -> float
  .average_travel_time -> float
  .valid_paths_count -> int  # Number of paths within distance constraints
  .summary() -> str
```

### LabType

```python
LabType.STANDARD    # 1.0x speed, 100% drain, 60kW, 2 slots
LabType.BIOLAB      # 2.0x speed, 50% drain, 300kW, 4 slots (Space Age)

# Properties
  .speed_multiplier -> float
  .science_drain -> float (0.0 to 1.0)
  .effective_speed -> float  # speed / drain
  .energy_consumption_kw -> float
  .module_slots -> int
  .cost -> int
```

### Lab

```python
Lab(position, lab_type=LabType.STANDARD)
  .position -> Point
  .lab_type -> LabType
  .cost -> int
  .speed_multiplier -> float
  .science_drain -> float
  .effective_speed -> float
  .energy_consumption_kw -> float
  .module_slots -> int
  .describe() -> str
```

### LabCluster

```python
LabCluster(labs)
  .labs -> List[Lab]
  .lab_count -> int
  .biolab_count() -> int
  .total_cost -> int
  .total_energy_consumption_kw -> float
  .average_speed_multiplier -> float
  .average_science_drain -> float
  .average_effective_speed -> float
  .total_module_slots -> int
  .summary() -> str
```

## Features

- ✅ Multi-belt-type support (yellow, red, blue)
- ✅ Underground belt routing with distance validation
- ✅ Ground belt materials with movement bonuses
- ✅ Research labs (standard and biolab) with efficiency modeling
- ✅ A* pathfinding with manhattan distance heuristic
- ✅ Automatic path cost calculation with turn penalties
- ✅ Network-level metrics and analysis
- ✅ Grid visualization
- ✅ Modular architecture for extension
- ✅ Factorio wiki references for all models

## Future Enhancements

- Support for splitters and mergers
- Blueprint export to Factorio format
- Multi-lane belt routing
- Cost-optimized routing strategies
- Interactive layout editor
- Assembler/crafter integration
- Supply chain optimization
