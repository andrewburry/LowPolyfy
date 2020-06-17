import logging

logger = logging.getLogger(__name__)

class DynamicBoxBinner():
    def __init__(self, length, width, height):
        self.dimensions = (length, width, height)
        self.num_bins = 1

        logger.info("Creating a box of dimension {} containing {} bins".format(self.dimensions, num_bins))
        self.dimensions = dimensions

    def filter_points(self, points):
        return points