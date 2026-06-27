"""Grid and pathfinding utilities for belt routing."""

from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, Iterable, List, Optional, Set, Tuple

Point = Tuple[int, int]


class Grid:
    width: int
    height: int
    obstacles: Set[Point]
    occupied: Set[Point]

    def __init__(
        self, width: int, height: int, obstacles: Optional[Iterable[Point]] = None
    ):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles or [])
        self.occupied = set()

    def contains(self, point: Point) -> bool:
        x, y = point
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, point: Point) -> bool:
        return (
            self.contains(point)
            and point not in self.obstacles
            and point not in self.occupied
        )

    def reserve(self, path: List[Point]) -> None:
        self.occupied.update(path)

    def neighbors(self, point: Point) -> Iterable[Point]:
        x, y = point
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = (x + dx, y + dy)
            if self.is_walkable(neighbor):
                yield neighbor

    def render(
        self,
        links: List[object],
        paths: Dict[str, List[Point]],
        labs: Optional[List[object]] = None,
    ) -> str:
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        for x, y in self.obstacles:
            grid[y][x] = "#"

        # mark labs specially (override obstacle char) using their footprint
        if labs:
            for lab in labs:
                try:
                    tiles = lab.footprint()
                except Exception:
                    tiles = [getattr(lab, "position", None)]
                lab_type_name = getattr(getattr(lab, "lab_type", None), "name", "")
                mark = "B" if lab_type_name.upper() == "BIOLAB" else "L"
                for lx, ly in tiles:
                    if 0 <= lx < self.width and 0 <= ly < self.height:
                        grid[ly][lx] = mark

        for link in links:
            sx, sy = link.source
            tx, ty = link.target
            grid[sy][sx] = "S"
            grid[ty][tx] = "T"

        for path in paths.values():
            for x, y in path:
                if grid[y][x] in ("S", "T"):
                    continue
                grid[y][x] = "*"

        return "\n".join("".join(row) for row in grid)


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid: Grid, start: Point, target: Point) -> Optional[List[Point]]:
    open_set: List[Tuple[int, int, Point]] = []
    heappush(open_set, (manhattan(start, target), 0, start))

    came_from: Dict[Point, Point] = {}
    g_score: Dict[Point, int] = {start: 0}

    while open_set:
        _, current_cost, current = heappop(open_set)

        if current == target:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in grid.neighbors(current):
            tentative_cost = current_cost + 1
            if tentative_cost < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_cost
                priority = tentative_cost + manhattan(neighbor, target)
                heappush(open_set, (priority, tentative_cost, neighbor))

    return None
