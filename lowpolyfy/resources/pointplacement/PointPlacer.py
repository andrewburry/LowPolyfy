import logging
from lowpolyfy.resources.pointplacement.random.PointsRandom import PointsRandom
from lowpolyfy.resources.pointplacement.box.v1.PointsBoxFeatures import PointsBoxFeatures
from lowpolyfy.resources.pointplacement.box.v1.PointsBoxRandom import PointsBoxRandom
from lowpolyfy.resources.pointplacement.box.v2.PointsBoxDynamic import PointsBoxDynamic

logger = logging.getLogger(__name__)

class PointPlacer():
    def __init__(self, video):
        self._ALGORTIHMS = {
            "random": PointsRandom,
            "boxfeaturedynamic": PointsBoxDynamic,
            "boxfeature": PointsBoxFeatures,
            "boxrandom": PointsBoxRandom
        }
        self._algorithm = None
        self.video = video

    def set_algorithm(self, name: str) -> bool:
        if (name not in self._ALGORTIHMS.keys()):
            logger.error("Could not find an algorithm with the name {}.".format(name))
            return False

        self._algorithm = self._ALGORTIHMS[name]
        return True

    def place_points(self, video_cube, num_points: int):
        if not self._algorithm:
            logger.eror("You must first set an algorithm to run.")
            return
        points = self._algorithm().generate_points(video_cube.dimensions, num_points, self.video)
        video_cube.add_points(points)