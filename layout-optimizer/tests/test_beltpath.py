import unittest

from model import BeltPath, BeltSegment, BeltType, UndergroundBeltType


class TestBeltPath(unittest.TestCase):
    def test_mixed_segments(self):
        seg1 = BeltSegment(
            [(0, 0), (1, 0), (2, 0)], mode="belt", belt_type=BeltType.RED
        )
        seg2 = BeltSegment(
            [(2, 0), (3, 0), (4, 0)],
            mode="underground",
            underground_type=UndergroundBeltType.YELLOW,
        )
        path = BeltPath((0, 0), (4, 0), segments=[seg1, seg2])

        self.assertEqual(path.length, 4)
        self.assertEqual(path.turns, 0)
        self.assertAlmostEqual(path.travel_time, 0.2, places=6)
        self.assertAlmostEqual(path.capacity, 15.0, places=6)
        self.assertAlmostEqual(path.cost, 22.0, places=6)


if __name__ == "__main__":
    unittest.main()
