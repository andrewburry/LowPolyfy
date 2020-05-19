from lowpolyfy.pointplacement.PointsRandom import PointsRandom
import logging

logger = logging.getLogger(__name__)

class PointPlacer():
    def __init__(self):
        self._ALGORTIHMS = {
            "random": PointsRandom
        }
        self._algorithm = None

    def set_algorithm(self, name):
        if (name not in self._ALGORTIHMS.keys()):
            logger.error("Could not find an algorithm with the name {}.".format(name))
            return False

        self._algorithm = self._ALGORTIHMS[name]
        return True

    def place_points(self, video_cube, num_points):
        if not self._algorithm:
            logger.eror("You must first set an algorithm to run.")
            return
        points = self._algorithm().generate_points(video_cube.dimensions, num_points)        
        video_cube.add_points(points)