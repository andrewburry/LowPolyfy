from numpy.random import randint
from lowpolyfy.resources.pointplacement.AbstractAlgorithm import AbstractAlgorithm
from lowpolyfy.resources.pointplacement.box.v1.BoxBinner import BoxBinner
from lowpolyfy.resources.pointplacement.box.utils.FeaturePointCollector import FeaturePointCollector
import logging
from cv2 import goodFeaturesToTrack, CAP_PROP_POS_FRAMES, cvtColor, COLOR_BGR2GRAY
import numpy as np

logger = logging.getLogger(__name__)

class PointsBoxFeatures(AbstractAlgorithm):
    def generate_points(self, dimensions, num_points, video):
        logger.info("Generating {} points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        # Generate points from features in the video
        points = FeaturePointCollector().generate_keypoints_from_features(video)

        # Create the box binner
        binner = BoxBinner(l, w, h, num_points)

        # Place points into boxes
        points = binner.filter_points(points)

        return points
