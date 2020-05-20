from numpy.random import randint
from lowpolyfy.resources.pointplacement.AbstractAlgorithm import AbstractAlgorithm
import logging

logger = logging.getLogger(__name__)

class PointsRandom(AbstractAlgorithm):

    def _generate_point(self, length, width, height):
        return [
            randint(0, length),
            randint(0, width),
            randint(0, height),
        ]

    def generate_points(self, dimensions, num_points):
        logger.info("Generating {} random points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        points = []

        for i in range(num_points):
            point = self._generate_point(l, w, h)
            points.append(point)

        return points
