import logging
from numpy.random import randint
from lowpolyfy.resources.pointplacement.AbstractAlgorithm import AbstractAlgorithm
from lowpolyfy.resources.pointplacement.box.v1.BoxBinner import BoxBinner
from cv2 import goodFeaturesToTrack, CAP_PROP_POS_FRAMES, cvtColor, COLOR_BGR2GRAY

logger = logging.getLogger(__name__)

class PointsBoxRandom(AbstractAlgorithm):
    def generate_points(self, dimensions, num_points, video):
        logger.info("Generating {} points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        # Start with no points
        points = []

        # Create the box binner
        binner = BoxBinner(l, w, h, num_points)

        # Place points into boxes
        # Note: the box binner will place random points by default into each box if they are empty!
        points = binner.filter_points(points)

        return points
