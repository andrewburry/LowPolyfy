from lowpolyfy.pointplacement.PointsRandom import PointsRandom

class PointPlacer():
    def __init__(self):
        self._ALGORTIHMS = {
            "random": PointsRandom
        }
        self._algorithm = None

    def set_algorithm(self, name):
        if (name not in self._ALGORTIHMS.keys()):
            print("Could not find an algorithm with this name.")
            return False

        self._algorithm = self._ALGORTIHMS[name]
        return True

    def place_points(self, video_cube, num_points):
        if not self._algorithm:
            print("You must set an algorithm to run")
            return
        points = self._algorithm().generate_points(video_cube.dimensions, num_points)        
        video_cube.add_points(points)