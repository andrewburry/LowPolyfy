from random import choice, randint

class SubdividingBox():
    def __init__(self, origin, dimensions, subdivideThreshold, depthThreshold, depth):
        self.origin = origin

        self.dimensions = dimensions
        self.subdivideThreshold = subdivideThreshold
        self.depthThreshold = depthThreshold

        self.boxes = []
        self.points = []
        self.depth = depth

        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def insert(self, point):
        # Check if it can be in this box
        if not self._dimension_check(point):
            return False

        # Check if we have boxes
        if len(self.boxes) > 0:
            # TODO: add to boxes instead
            self._insert_point_in_boxes(point)
        else:
            # Just add point to points if we have no boxes
            # This may involve subdividing
            self._add_to_self(point)
        return True

    def _dimension_check(self, point):
        x, y, z = point
        # Check to see if the point can be placed in me
        if ((x >= self.origin[0] and x <= self.origin[0] + self.dimensions[0]) and
            (y >= self.origin[1] and y <= self.origin[1] + self.dimensions[1]) and
            (z >= self.origin[2] and z <= self.origin[2] + self.dimensions[2])):
            return True
        return False
    
    
    def _add_to_self(self, point):
        # Add the point to the list of points
        self.points.append(point)

        # If the box has too many points, subdivide it along the longest axis
        if len(self.points) >= self.subdivideThreshold and self.depth <= self.depthThreshold:
            self.subdivide()
        
        return
    
    def subdivide(self):
        # Subdivide the current box on the longest dimension
        sides = list(self.dimensions)
        longestSideIndex = sides.index(max(sides))

        # Now we know which dimension to cut in half
        sides[longestSideIndex] /= 2

        # Now we can create two boxes, one will be centered on the same origin as the parent
        # The second will be shifted by half the longest side
        shiftOrigin = list(self.origin)
        shiftOrigin[longestSideIndex] += sides[longestSideIndex]
        box1 = SubdividingBox(self.origin, tuple(sides), self.subdivideThreshold, self.depthThreshold, self.depth + 1)
        box2 = SubdividingBox(tuple(shiftOrigin), tuple(sides), self.subdivideThreshold, self.depthThreshold, self.depth + 1)

        self.boxes.append(box1)
        self.boxes.append(box2)

        # Now we need to sort the points into their respective boxes
        self.sortPoints()
        return

    def sortPoints(self):
        # Insert the points into boxes
        for point in self.points:
            self._insert_point_in_boxes(point)

        # the box does not need to keep track of points anymore
        self.points = []
        return

    def _insert_point_in_boxes(self, point):
        # Try to insert into box0, if it fails insert into box1
        # Note: they perform dimensional checks themselves
        if not self.boxes[0].insert(point):
            return self.boxes[1].insert(point)
        return False

    def fetch_random_points(self):
        # Recursively call fetch points on sub boxes
        if len(self.boxes) > 0:
            return self.boxes[0].fetch_random_points() + self.boxes[1].fetch_random_points()

        # Select a random point that the current box contains
        if len(self.points) > 0:
            return [choice(self.points)]

        # Empty box
        # TODO: maybe generate a point
        return []

    def fetch_all_points(self):
        # Recursively call fetch points on sub boxes
        if len(self.boxes) > 0:
            return self.boxes[0].fetch_all_points() + self.boxes[1].fetch_all_points()

        # Return all points
        return self.points

    def fetch_all_boxes(self):
        if len(self.boxes) > 0:
            return self.boxes[0].fetch_all_boxes() + self.boxes[1].fetch_all_boxes() + [self]
        
        return [self]

    def fetch_end_point_boxes(self):
        if len(self.boxes) > 0:
            return self.boxes[0].fetch_end_point_boxes() + self.boxes[1].fetch_end_point_boxes()

        return [self]

    def is_visible_on_frame(self, frame_number):
        length, _, _ = self.dimensions
        origin_frame, _, _ = self.origin

        if frame_number < origin_frame or frame_number > origin_frame + length:
            return False

        return True

    def get_polygon(self):
        origin = [round(number) for number in self.origin]
        dimensions = [round(number) for number in self.dimensions]

        p1 = [origin[1]                , origin[2]]
        p2 = [origin[1] + dimensions[1], origin[2]]
        p4 = [origin[1]                , origin[2] + dimensions[2]]
        p3 = [origin[1] + dimensions[1], origin[2] + dimensions[2]]

        return [p1, p2, p3, p4]

    def generate_random_point(self):
        return
