from sympy import Point3D, Plane, Segment3D
from itertools import combinations

def _create_points(tetrahedral):
    points = []
    # Create point objects for calculating line-plane intersections
    for corner_point in tetrahedral:
        point = Point3D(corner_point)
        points.append(point)
    return points

def _create_tetrahedral_line_segments(corners):
    # Create the point objects for the tetrahedral corners
    points = _create_points(corners)

    # Take every combination of corner points of length 2
    point_combinations = list(combinations(corners, 2))

    lines = []
    # Create line segments for each combination of points
    for combination in point_combinations:
        point1 = combination[0]
        point2 = combination[1]
        line = Segment3D(point1, point2)
        lines.append(line)
    return lines


def _intersect_line_plane(line, plane):
    # Intersection could be empty, a segment or a point
    # TODO: This intersection operation is extremely slow. Consider making my own.
    intersections = line.intersection(plane)

    # If the intersection is empty then just return
    if not intersections:
        return intersections

    # Extract the points of a line segment
    if (type(intersections[0]) is Segment3D):
        return list(intersections[0].points)

    return intersections

def check_frame_bounded(points, frame_number):
    # Ensure that points are crossing the frame number at least once
    lower_bounded = False
    upper_bounded = False
    for point in points:
        if point[0] <= frame_number:
            lower_bounded = True
        elif point[0] > frame_number:
            upper_bounded = True

    return lower_bounded and upper_bounded



def find_tetrahedral_frame_intersections(corners, frame_number):
    # Check to see if the frame is bounded by the corners
    if(not check_frame_bounded(corners, frame_number)):
        return []

    # Define a plane in the video cube corresponding to the frame of interest
    plane = Plane(Point3D(frame_number, 0, 0), 
                  Point3D(frame_number, 1, 0), 
                  Point3D(frame_number, 0, 1))

    # Create the line segments that form the tetrahedral
    lines = _create_tetrahedral_line_segments(corners)

    # Find the intersection of each line and the plane
    intersections = []
    for line in lines:
        inter = _intersect_line_plane(line, plane)
        intersections = intersections + inter

    # Remove any duplicate points
    intersections = list(dict.fromkeys(intersections))

    return intersections