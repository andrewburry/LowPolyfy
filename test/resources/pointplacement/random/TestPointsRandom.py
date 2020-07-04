import unittest
from lowpolyfy.resources.pointplacement.random.PointsRandom import PointsRandom

class test_pointsrandom(unittest.TestCase):

    def test_generate_points(self):
        dimensions = (10, 10, 10)
        numPoints = 100
        pointsRandom = PointsRandom()

        points = pointsRandom.generate_points(dimensions, numPoints, None)

        self.assertTrue(len(points) == numPoints)


if __name__ == '__main__':
    unittest.main()