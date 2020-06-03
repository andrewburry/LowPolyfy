from numpy.random import randint
from lowpolyfy.resources.pointplacement.AbstractAlgorithm import AbstractAlgorithm
import logging
from cv2 import goodFeaturesToTrack, CAP_PROP_POS_FRAMES, cvtColor, COLOR_BGR2GRAY
import numpy as np

logger = logging.getLogger(__name__)

class PointsPoissonDisk(AbstractAlgorithm):

    def __init__(self):
        self.maxCorners = 1000
        self.qualityLevel = 0.0001
        self.minDistance = 10

    def _generate_points_from_features(self, video):
        points = []

        # Loop through the 
        frame_number = 0
        while video.isOpened():
            # Read a frame of the video
            frames_remain, frame = video.read()

            # Stop reading if we reach the end of the video
            if not frames_remain:
                break
            
            gray = cvtColor(frame, COLOR_BGR2GRAY)
            discovered_points = goodFeaturesToTrack(gray, self.maxCorners, self.qualityLevel, self.minDistance)
            for point in discovered_points:
                y, x = point.ravel()
                points.append([frame_number, int(y), int(x)])

            frame_number += 1
    
        # Reset the video capture to frame 0
        video.set(CAP_PROP_POS_FRAMES, 0)
        return points

    def generate_points(self, dimensions, num_points, video):
        logger.info("Generating {} random points within a space of dimension {}".format(num_points, dimensions))
        l, w, h = dimensions

        # Generate points from features in the video
        points = self._generate_points_from_features(video)

        # TODO: Place points into boxes and pick a point from the bins to survive

        return points
