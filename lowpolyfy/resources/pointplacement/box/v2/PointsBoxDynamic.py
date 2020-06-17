
from lowpolyfy.resources.pointplacement.box.v2.DynamicBoxBinner import DynamicBoxBinner
import logging

logger = logging.getLogger(__name__)

class PointsBoxDynamic():
    def __init__(self):
        self.maxCorners = 1000
        self.qualityLevel = 0.0001
        self.minDistance = 10

    def generate_points(self, dimensions, num_points, video):
        logger.info("Generating {} points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        # Start with no points
        points = []

        # Create the box binner
        binner = DynamicBoxBinner(l, w, h)

        # Place points into boxes
        points = binner.filter_points(points)

        return points