import unittest

from model import Lab, LabType


class TestLab(unittest.TestCase):
    def test_biolab_footprint_is_five_by_five(self):
        lab = Lab((10, 20), LabType.BIOLAB)

        self.assertEqual(LabType.BIOLAB.dimensions, (5, 5))
        self.assertEqual(lab.dimensions, (5, 5))
        self.assertEqual(len(lab.footprint()), 25)
        self.assertIn((14, 24), lab.footprint())


if __name__ == "__main__":
    unittest.main()
