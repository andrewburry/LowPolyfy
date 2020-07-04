import unittest
from lowpolyfy.resources.pointplacement.PointPlacer import PointPlacer

class test_pointplacer(unittest.TestCase):
    def test_set_algorithm(self):
        placer = PointPlacer(None)
        self.assertTrue(placer.set_algorithm("random"))
        self.assertFalse(placer.set_algorithm("NOT_AN_ALGORITHM"))

if __name__ == '__main__':
    unittest.main()