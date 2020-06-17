from lowpolyfy.resources.geometry.LineSegment import LineSegment
from collections import OrderedDict
from itertools import combinations

class Tetrahedral():
    def __init__(self, corners):
        self.corners = corners
        self._create_tetrahedral_line_segments(corners)

    def frames_intersected(self):
        points = []
        for line in self.lines:
            points += line.frames_intersected()
        
        # Remove duplicates
        return list(dict.fromkeys(points))

    def _create_tetrahedral_line_segments(self, corners):
        # Take every combination of corner points of length 2
        point_combinations = list(combinations(corners, 2))

        self.lines = []
        # Create line segments for each combination of points
        for combination in point_combinations:
            line = LineSegment(combination[0], combination[1])
            self.lines.append(line)
        return

    def _check_frame_bounded(self, points, frame_number):
        # Ensure that points are crossing the frame number at least once
        lower_bounded = False
        upper_bounded = False
        for point in points:
            if point[0] <= frame_number:
                lower_bounded = True
            elif point[0] > frame_number:
                upper_bounded = True

        return lower_bounded and upper_bounded

    def intersection(self, frame_number):
        # Check to see if the frame is bounded by the corners
        if(not self._check_frame_bounded(self.corners, frame_number)):
            return []

        # Find the intersection of each line and the frame plane
        intersections = []
        for line in self.lines:
            inter = line.intersection(frame_number)
            intersections = intersections + inter

        # Remove any duplicate points
        intersections = list(OrderedDict((tuple(x), x) for x in intersections).values())

        return intersections
    