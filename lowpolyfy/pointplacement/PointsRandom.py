from numpy.random import randint
from lowpolyfy.pointplacement.AbstractAlgorithm import AbstractAlgorithm

class PointsRandom(AbstractAlgorithm):

    def _generate_point(self, length, width, height):
        return [
            randint(0, length),
            randint(0, width),
            randint(0, height),
        ]

    def generate_points(self, dimensions, num_points):
        l, w, h = dimensions

        points = []

        for i in range(num_points):
            points.append(self._generate_point(l, w, h))

        return points
