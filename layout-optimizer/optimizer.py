"""Layout optimization logic for belt placement."""

from __future__ import annotations

from collections.abc import Iterable

try:
    from .grid import Grid, Point, a_star, manhattan
    from .model import BeltNetwork, BeltPath, BeltType, Lab, LabType, Link
except ImportError:
    from grid import Grid, Point, a_star, manhattan
    from model import BeltNetwork, BeltPath, BeltType, Lab, LabType, Link


class LayoutOptimizer:
    def __init__(
        self, width: int, height: int, obstacles: Iterable[Point] | None = None
    ):
        self.grid = Grid(width, height, obstacles)
        self.links: list[Link] = []
        self.labs: list[Lab] = []

    def _is_footprint_free(self, footprint: list[Point]) -> bool:
        for p in footprint:
            if not self.grid.contains(p):
                return False
            if p in self.grid.obstacles or p in self.grid.occupied:
                return False
        return True

    def find_free_position_for_lab(
        self,
        desired_pos: Point,
        lab_type: LabType = LabType.STANDARD,
        dimensions: tuple[int, int] | None = None,
        max_search_radius: int = 10,
    ) -> Point | None:
        """Search nearby positions for a free top-left placement for a lab footprint.

        Returns the first free position found within `max_search_radius`, or None.
        """
        if dimensions is None:
            dimensions = lab_type.dimensions
        x0, y0 = desired_pos
        for r in range(max_search_radius + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    # simple square search
                    cand = (x0 + dx, y0 + dy)
                    lab = Lab(cand, lab_type)
                    lab.dimensions = dimensions
                    if self._is_footprint_free(lab.footprint()):
                        return cand
        return None

    def add_link(
        self,
        source: Point,
        target: Point,
        name: str = "",
        belt_type: BeltType = BeltType.YELLOW,
    ) -> None:
        self.links.append(
            Link(source, target, name or f"{source}->{target}", belt_type)
        )

    def add_lab(self, position: Point, lab_type: LabType = LabType.STANDARD) -> None:
        """Add a lab as an obstacle in the layout.

        By default this treats `position` as the top-left tile of the lab footprint
        and reserves the entire footprint so routing avoids it. If the desired
        placement overlaps existing reserved tiles, a RuntimeError will be raised.
        """
        lab = Lab(position, lab_type)
        if not self._is_footprint_free(lab.footprint()):
            raise RuntimeError(f"Lab footprint at {position} overlaps reserved tiles")
        self.labs.append(lab)
        # reserve entire footprint so pathfinding avoids the lab tiles
        self.grid.obstacles.update(lab.footprint())

    def add_lab_obj(
        self, lab: Lab, auto_place: bool = False, max_search_radius: int = 10
    ) -> None:
        """Add a `Lab` object to the layout; reserves its footprint.

        If `auto_place` is True, will attempt to find a nearby free top-left
        position within `max_search_radius` if the current position overlaps.
        """
        if not self._is_footprint_free(lab.footprint()):
            if auto_place:
                new_pos = self.find_free_position_for_lab(
                    lab.position, lab.lab_type, lab.dimensions, max_search_radius
                )
                if new_pos is None:
                    raise RuntimeError("No free position found to place lab")
                lab.position = new_pos
            else:
                raise RuntimeError("Lab footprint overlaps reserved tiles")
        self.labs.append(lab)
        self.grid.obstacles.update(lab.footprint())

    def optimize(self) -> BeltNetwork:
        ordered_links = sorted(
            self.links, key=lambda link: manhattan(link.source, link.target)
        )
        paths: list[BeltPath] = []

        for link in ordered_links:
            temp_grid = Grid(self.grid.width, self.grid.height, self.grid.obstacles)
            temp_grid.occupied = set(self.grid.occupied)
            path_points = a_star(temp_grid, link.source, link.target)
            if path_points is None:
                raise RuntimeError(
                    f"No path found for link {link.name} from {link.source} to {link.target}"
                )

            self.grid.reserve(path_points)
            paths.append(
                BeltPath(
                    link.source, link.target, path_points, belt_type=link.belt_type
                )
            )

        return BeltNetwork(paths)

    def render(self, belt_network: BeltNetwork) -> str:
        paths = {
            f"{path.source}->{path.target}": path.path for path in belt_network.paths
        }
        return self.grid.render(self.links, paths, labs=self.labs)
