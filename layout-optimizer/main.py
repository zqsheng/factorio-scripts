"""Command-line entrypoint for the belt layout optimizer."""

from __future__ import annotations

try:
    from .model import BeltType, LabType
    from .optimizer import LayoutOptimizer
except ImportError:
    from model import BeltType, LabType
    from optimizer import LayoutOptimizer


def main() -> None:
    optimizer = LayoutOptimizer(
        width=50,
        height=50,
        obstacles={(7, y) for y in range(2, 10)},
    )
    optimizer.add_link((1, 1), (18, 2), "input-1", BeltType.RED)
    optimizer.add_link((1, 4), (18, 5), "input-2", BeltType.YELLOW)
    optimizer.add_link((1, 8), (18, 9), "input-3", BeltType.BLUE)
    # place a standard lab and a biolab as obstacles
    optimizer.add_lab((10, 6), LabType.STANDARD)
    optimizer.add_lab((14, 9), LabType.BIOLAB)

    network = optimizer.optimize()
    print(optimizer.render(network))
    print(network.summary())

    for path in network.paths:
        print(path.describe())


if __name__ == "__main__":
    main()
