"""Belt network mathematical model for Factorio layout optimization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

# Point alias for coordinates used across the models
Point = Tuple[int, int]


class BeltType(Enum):
    """Surface belt types and their speeds/costs."""

    YELLOW = {"speed": 15.0, "cost": 10}
    RED = {"speed": 30.0, "cost": 20}
    BLUE = {"speed": 45.0, "cost": 30}

    def __init__(self, properties: dict):
        self.speed = properties["speed"]
        self.cost = properties["cost"]

    def __str__(self) -> str:
        return self.name.lower()


class BeltSegment:
    """Segment of a belt path: either surface belt or underground segment."""

    def __init__(
        self,
        path: List[Point],
        mode: str = "belt",
        belt_type: Optional[BeltType] = None,
        underground_type: Optional["UndergroundBeltType"] = None,
        direction: Optional[Tuple[int, int]] = None,
    ):
        self.path = path
        self.mode = mode  # 'belt' or 'underground'
        self.belt_type = belt_type
        self.underground_type = underground_type
        # explicit direction (dx, dy) for the segment; if None, computed from first step
        self._direction = direction

    @property
    def length(self) -> int:
        return max(0, len(self.path) - 1)

    def travel_time(self) -> float:
        if self.mode == "belt":
            bt = self.belt_type or BeltType.YELLOW
            return self.length / bt.speed
        else:
            ut = self.underground_type
            if ut is None:
                # fallback to belt speed
                return self.length / BeltType.YELLOW.speed
            return self.length / ut.speed

    def cost(self) -> float:
        if self.mode == "belt":
            return float(self.length)
        else:
            ut = self.underground_type
            return float(self.length * (ut.cost_per_unit if ut is not None else 0))

    @property
    def direction(self) -> Optional[Tuple[int, int]]:
        """Return explicit direction if set, otherwise compute from the first step in path.

        Direction is a small (dx, dy) vector such as (1,0), (-1,0), (0,1), (0,-1).
        """
        if getattr(self, "_direction", None) is not None:
            return self._direction
        if len(self.path) >= 2:
            a, b = self.path[0], self.path[1]
            return (b[0] - a[0], b[1] - a[1])
        return None

    @direction.setter
    def direction(self, value: Optional[Tuple[int, int]]) -> None:
        self._direction = value


class BeltPath:
    """A belt path composed of one or more segments (surface belts and/or undergrounds).

    Backwards-compatible constructor: if `path` is provided (list of points) it
    will create a single surface belt segment using `belt_type`.
    """

    def __init__(
        self,
        source: Point,
        target: Point,
        path: Optional[List[Point]] = None,
        belt_type: Optional[BeltType] = None,
        turn_penalty: float = 2.0,
        segments: Optional[List[BeltSegment]] = None,
    ):
        self.source = source
        self.target = target
        self.turn_penalty = turn_penalty
        if segments is not None:
            self.segments = segments
        else:
            if path is None:
                path = [source, target]
            bt = belt_type or BeltType.YELLOW
            self.segments = [BeltSegment(path, "belt", belt_type=bt)]

    @property
    def full_path(self) -> List[Point]:
        pts: List[Point] = []
        for seg in self.segments:
            if not pts:
                pts.extend(seg.path)
            else:
                # avoid duplicating the connecting point
                pts.extend(seg.path[1:])
        return pts

    @property
    def length(self) -> int:
        return sum(seg.length for seg in self.segments)

    @property
    def turns(self) -> int:
        pts = self.full_path
        if len(pts) < 3:
            return 0
        count = 0
        for first, second, third in zip(pts, pts[1:], pts[2:]):
            current_direction = (second[0] - first[0], second[1] - first[1])
            next_direction = (third[0] - second[0], third[1] - second[1])
            if current_direction != next_direction:
                count += 1
        return count

    @property
    def travel_time(self) -> float:
        return sum(seg.travel_time() for seg in self.segments)

    @property
    def capacity(self) -> float:
        # conservative: capacity is minimum across segments (underground or belt)
        caps: List[float] = []
        for seg in self.segments:
            if seg.mode == "belt":
                caps.append((seg.belt_type or BeltType.YELLOW).speed)
            else:
                caps.append(
                    (
                        seg.underground_type.speed
                        if seg.underground_type is not None
                        else BeltType.YELLOW.speed
                    )
                )
        return min(caps) if caps else 0.0

    @property
    def cost(self) -> float:
        # surface belts: cost per tile = 1; underground segments use their cost_per_unit
        seg_costs = sum(seg.cost() for seg in self.segments)
        return seg_costs + self.turn_penalty * float(self.turns)

    def describe(self) -> str:
        return (
            f"BeltPath({self.source} -> {self.target}, length={self.length}, "
            f"turns={self.turns}, travel_time={self.travel_time:.2f}s, "
            f"capacity={self.capacity:.1f}, cost={self.cost:.1f})"
        )

    @property
    def path(self) -> List[Point]:
        """Backward-compatible alias for the full path points."""
        return self.full_path


@dataclass
class Link:
    source: Point
    target: Point
    name: str = ""
    belt_type: BeltType = BeltType.YELLOW


@dataclass
class BeltNetwork:
    paths: List[BeltPath]

    @property
    def total_length(self) -> int:
        return sum(path.length for path in self.paths)

    @property
    def total_turns(self) -> int:
        return sum(path.turns for path in self.paths)

    @property
    def average_travel_time(self) -> float:
        if not self.paths:
            return 0.0
        return sum(path.travel_time for path in self.paths) / len(self.paths)

    @property
    def bottleneck_capacity(self) -> float:
        if not self.paths:
            return 0.0
        return min(path.capacity for path in self.paths)

    @property
    def total_cost(self) -> float:
        return sum(path.cost for path in self.paths)

    def summary(self) -> str:
        return (
            f"BeltNetwork(total_length={self.total_length}, total_turns={self.total_turns}, "
            f"avg_travel_time={self.average_travel_time:.2f}s, "
            f"bottleneck_capacity={self.bottleneck_capacity:.1f}, "
            f"total_cost={self.total_cost:.1f})"
        )


class GroundBeltType(Enum):
    """Ground belt materials with movement speed, cost, and crossing width.

    Movement speed multiplier:
    - 1.0 = normal speed
    - > 1.0 = faster movement

    Maximum cross tile:
    - Width in tiles that characters can cross on the ground belt
    """

    STONE = {"speed_multiplier": 1.0, "cost": 1, "maximum_cross_tile": 1}
    CONCRETE = {"speed_multiplier": 1.15, "cost": 5, "maximum_cross_tile": 2}
    REFINED_CONCRETE = {"speed_multiplier": 1.25, "cost": 10, "maximum_cross_tile": 3}
    HAZARD_CONCRETE = {"speed_multiplier": 1.25, "cost": 12, "maximum_cross_tile": 3}

    def __init__(self, properties: dict):
        self.speed_multiplier = properties["speed_multiplier"]
        self.cost_per_tile = properties["cost"]
        self.maximum_cross_tile = properties["maximum_cross_tile"]

    def __str__(self) -> str:
        return self.name.lower().replace("_", " ")


@dataclass
class GroundBelt:
    """Single ground belt tile with material and properties."""

    position: Point
    material: GroundBeltType = GroundBeltType.STONE
    direction: Optional[Tuple[int, int]] = None

    @property
    def cost(self) -> int:
        return self.material.cost_per_tile

    @property
    def speed_boost(self) -> float:
        return self.material.speed_multiplier

    @property
    def maximum_cross_tile(self) -> int:
        return self.material.maximum_cross_tile

    def describe(self) -> str:
        return (
            f"GroundBelt({self.position}, material={self.material}, "
            f"speed_boost={self.speed_boost:.2f}x, cost={self.cost}, "
            f"max_cross={self.maximum_cross_tile}, direction={self.direction})"
        )


@dataclass
class GroundBeltPath:
    """Path of ground belts connecting two points."""

    source: Point
    target: Point
    path: List[Point]
    material: GroundBeltType = GroundBeltType.STONE

    @property
    def length(self) -> int:
        return max(0, len(self.path) - 1)

    @property
    def total_cost(self) -> int:
        return self.length * self.material.cost_per_tile

    @property
    def average_speed_multiplier(self) -> float:
        return self.material.speed_multiplier

    @property
    def maximum_cross_tile(self) -> int:
        return self.material.maximum_cross_tile

    def describe(self) -> str:
        return (
            f"GroundBeltPath({self.source} -> {self.target}, material={self.material}, "
            f"length={self.length}, speed_mult={self.average_speed_multiplier:.2f}x, "
            f"max_cross={self.maximum_cross_tile}, total_cost={self.total_cost})"
        )


@dataclass
class GroundBeltNetwork:
    """Complete ground belt network analysis."""

    paths: List[GroundBeltPath]

    @property
    def total_length(self) -> int:
        return sum(path.length for path in self.paths)

    @property
    def total_cost(self) -> int:
        return sum(path.total_cost for path in self.paths)

    @property
    def average_speed_multiplier(self) -> float:
        if not self.paths:
            return 1.0
        total_mult = sum(
            path.average_speed_multiplier * path.length for path in self.paths
        )
        return total_mult / self.total_length if self.total_length > 0 else 1.0

    @property
    def cost_per_tile(self) -> float:
        if self.total_length == 0:
            return 0.0
        return self.total_cost / self.total_length

    def summary(self) -> str:
        return (
            f"GroundBeltNetwork(total_length={self.total_length}, "
            f"total_cost={self.total_cost}, "
            f"avg_speed_mult={self.average_speed_multiplier:.2f}x, "
            f"cost_per_tile={self.cost_per_tile:.1f})"
        )


class UndergroundBeltType(Enum):
    """Underground belt types for Factorio.

    Reference: https://wiki.factorio.com/Underground_belt

    Underground belts allow transport belts to cross underneath other belts.
    Maximum underground distance: 4 squares
    Speed is the same as the corresponding belt type.
    Cannot transport items beneath lava (Space Age) and space void.
    """

    YELLOW = {"speed": 15.0, "cost": 10, "max_distance": 4}
    RED = {"speed": 30.0, "cost": 20, "max_distance": 4}
    BLUE = {"speed": 45.0, "cost": 30, "max_distance": 4}

    def __init__(self, properties: dict):
        self.speed = properties["speed"]
        self.cost_per_unit = properties["cost"]
        self.max_distance = properties["max_distance"]

    def __str__(self) -> str:
        return self.name.lower()


@dataclass
class UndergroundBelt:
    """Single underground belt tile.

    Underground belts are components that allow belts to cross beneath other belts.
    """

    position: Point
    belt_type: UndergroundBeltType = UndergroundBeltType.YELLOW
    direction: Optional[Tuple[int, int]] = None

    @property
    def cost(self) -> int:
        return self.belt_type.cost_per_unit

    @property
    def speed(self) -> float:
        return self.belt_type.speed

    @property
    def max_distance(self) -> int:
        return self.belt_type.max_distance

    def describe(self) -> str:
        return (
            f"UndergroundBelt({self.position}, type={self.belt_type}, "
            f"speed={self.speed:.1f}, max_distance={self.max_distance}, cost={self.cost}, "
            f"direction={self.direction})"
        )


@dataclass
class UndergroundBeltPath:
    """Path of underground belts connecting two points.

    Reference: https://wiki.factorio.com/Underground_belt
    """

    source: Point
    target: Point
    path: List[Point]
    belt_type: UndergroundBeltType = UndergroundBeltType.YELLOW

    @property
    def length(self) -> int:
        return max(0, len(self.path) - 1)

    @property
    def total_cost(self) -> int:
        return self.length * self.belt_type.cost_per_unit

    @property
    def speed(self) -> float:
        return self.belt_type.speed

    @property
    def capacity(self) -> float:
        return self.belt_type.speed

    @property
    def travel_time(self) -> float:
        return self.length / self.belt_type.speed

    def is_valid_distance(self) -> bool:
        """Check if path respects maximum underground distance constraint."""
        return self.length <= self.belt_type.max_distance

    def describe(self) -> str:
        validity = "✓" if self.is_valid_distance() else "✗"
        return (
            f"UndergroundBeltPath({self.source} -> {self.target}, type={self.belt_type}, "
            f"length={self.length}/{self.belt_type.max_distance} {validity}, "
            f"speed={self.speed:.1f}, capacity={self.capacity:.1f}, "
            f"travel_time={self.travel_time:.2f}s, cost={self.total_cost})"
        )


@dataclass
class UndergroundBeltNetwork:
    """Network of underground belts with distance validation.

    Reference: https://wiki.factorio.com/Underground_belt
    """

    paths: List[UndergroundBeltPath]

    @property
    def total_length(self) -> int:
        return sum(path.length for path in self.paths)

    @property
    def total_cost(self) -> int:
        return sum(path.total_cost for path in self.paths)

    @property
    def total_capacity(self) -> float:
        return sum(path.capacity for path in self.paths)

    @property
    def bottleneck_capacity(self) -> float:
        if not self.paths:
            return 0.0
        return min(path.capacity for path in self.paths)

    @property
    def average_travel_time(self) -> float:
        if not self.paths:
            return 0.0
        return sum(path.travel_time for path in self.paths) / len(self.paths)

    @property
    def valid_paths_count(self) -> int:
        return sum(1 for path in self.paths if path.is_valid_distance())

    def summary(self) -> str:
        validity = f"{self.valid_paths_count}/{len(self.paths)}"
        return (
            f"UndergroundBeltNetwork(total_length={self.total_length}, "
            f"valid_paths={validity}, total_cost={self.total_cost}, "
            f"bottleneck_capacity={self.bottleneck_capacity:.1f}, "
            f"avg_travel_time={self.average_travel_time:.2f}s)"
        )


class LabType(Enum):
    """Research lab types for Factorio.

    Reference: https://wiki.factorio.com/Lab and https://wiki.factorio.com/Biolab

    Labs are research facilities that consume science packs and produce research progress.
    """

    STANDARD = {
        "name": "Lab",
        "speed_multiplier": 1.0,
        "science_drain": 1.0,  # 100% consumption
        "energy_consumption_kw": 60.0,
        "module_slots": 2,
        "cost": 10,
        "dimensions": (2, 2),
    }
    BIOLAB = {
        "name": "Biolab",
        "speed_multiplier": 2.0,  # 100% speed bonus (double research speed)
        "science_drain": 0.5,  # 50% consumption (half the packs)
        "energy_consumption_kw": 300.0,
        "module_slots": 4,
        "cost": 100,  # Representative cost
        "dimensions": (3, 3),
    }

    def __init__(self, properties: dict):
        self.lab_name = properties["name"]
        self.speed_multiplier = properties["speed_multiplier"]
        self.science_drain = properties["science_drain"]
        self.energy_consumption_kw = properties["energy_consumption_kw"]
        self.module_slots = properties["module_slots"]
        self.cost = properties["cost"]
        # footprint dimensions (width, height) in tiles
        self.dimensions = properties.get("dimensions", (1, 1))

    @property
    def effective_speed(self) -> float:
        """Effective research speed: speed / science_drain ratio."""
        return self.speed_multiplier / self.science_drain

    def __str__(self) -> str:
        return self.lab_name


@dataclass
class Lab:
    """Single research lab facility.

    Reference: https://wiki.factorio.com/Lab
    """

    position: Point
    lab_type: LabType = LabType.STANDARD
    dimensions: Optional[Tuple[int, int]] = None

    @property
    def cost(self) -> int:
        return self.lab_type.cost

    @property
    def speed_multiplier(self) -> float:
        return self.lab_type.speed_multiplier

    @property
    def science_drain(self) -> float:
        return self.lab_type.science_drain

    @property
    def effective_speed(self) -> float:
        return self.lab_type.effective_speed

    @property
    def energy_consumption_kw(self) -> float:
        return self.lab_type.energy_consumption_kw

    @property
    def module_slots(self) -> int:
        return self.lab_type.module_slots

    def describe(self) -> str:
        return (
            f"Lab({self.position}, type={self.lab_type}, "
            f"speed={self.speed_multiplier:.1f}x, drain={self.science_drain:.1%}, "
            f"effective_speed={self.effective_speed:.2f}x, "
            f"power={self.energy_consumption_kw:.0f}kW, slots={self.module_slots}, cost={self.cost})"
        )

    def __post_init__(self) -> None:
        if self.dimensions is None:
            self.dimensions = self.lab_type.dimensions

    def footprint(self) -> List[Point]:
        """Return list of tiles (x,y) occupied by this lab.

        The `position` is treated as the top-left corner of the footprint.
        """
        w, h = self.dimensions
        x0, y0 = self.position
        return [(x0 + dx, y0 + dy) for dx in range(w) for dy in range(h)]


@dataclass
class LabCluster:
    """Cluster of research labs for coordinated research.

    Reference: https://wiki.factorio.com/Lab
    """

    labs: List[Lab]

    @property
    def lab_count(self) -> int:
        return len(self.labs)

    @property
    def total_cost(self) -> int:
        return sum(lab.cost for lab in self.labs)

    @property
    def total_energy_consumption_kw(self) -> float:
        return sum(lab.energy_consumption_kw for lab in self.labs)

    @property
    def average_speed_multiplier(self) -> float:
        if not self.labs:
            return 0.0
        return sum(lab.speed_multiplier for lab in self.labs) / len(self.labs)

    @property
    def average_science_drain(self) -> float:
        if not self.labs:
            return 0.0
        return sum(lab.science_drain for lab in self.labs) / len(self.labs)

    @property
    def average_effective_speed(self) -> float:
        if not self.labs:
            return 0.0
        return sum(lab.effective_speed for lab in self.labs) / len(self.labs)

    @property
    def total_module_slots(self) -> int:
        return sum(lab.module_slots for lab in self.labs)

    def biolab_count(self) -> int:
        return sum(1 for lab in self.labs if lab.lab_type == LabType.BIOLAB)

    def summary(self) -> str:
        biolab_cnt = self.biolab_count()
        return (
            f"LabCluster(labs={self.lab_count}, biolabs={biolab_cnt}, "
            f"avg_speed={self.average_speed_multiplier:.1f}x, "
            f"avg_effective_speed={self.average_effective_speed:.2f}x, "
            f"total_power={self.total_energy_consumption_kw:.0f}kW, "
            f"total_cost={self.total_cost})"
        )
