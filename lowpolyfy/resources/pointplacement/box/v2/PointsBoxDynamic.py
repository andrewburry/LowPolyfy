import logging
from lowpolyfy.resources.pointplacement.box.v2.DynamicBoxBinner import DynamicBoxBinner
from lowpolyfy.resources.pointplacement.box.utils.FeaturePointCollector import FeaturePointCollector

logger = logging.getLogger(__name__)

class PointsBoxDynamic():
    def generate_points(self, dimensions, num_points, video):
        l, w, h = dimensions

        # Generate points from features in the video
        points = FeaturePointCollector().generate_keypoints_from_features(video)
        logger.info("Generated {} feature points within the video cube of dimensions".format(len(points), dimensions))
        # Create the box binner
        binner = DynamicBoxBinner(l, w, h)
        

        # Place points into the binner
        logger.info("Inserting {} points into the box binner".format(len(points)))
        points = binner.filter_points(points)
        logger.info("Returning {} points from the box binner".format(len(points)))

        return points