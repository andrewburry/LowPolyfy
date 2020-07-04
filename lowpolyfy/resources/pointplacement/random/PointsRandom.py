import logging
from numpy.random import randint
from lowpolyfy.resources.pointplacement.AbstractAlgorithm import AbstractAlgorithm

logger = logging.getLogger(__name__)

class PointsRandom(AbstractAlgorithm):
    def _generate_point(self, length: int, width: int, height: int) -> list:
        return [
            randint(0, length),
            randint(0, width),
            randint(0, height),
        ]

    def generate_points(self, dimensions: tuple, num_points: int, video) -> list:
        logger.info("Generating {} random points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        points = []

        for i in range(num_points):
            point = self._generate_point(l, w, h)
            points.append(point)

        return points
