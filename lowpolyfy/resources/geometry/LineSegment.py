class LineSegment():
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.x0, self.y0, self.z0 = tuple(self.p0)
        self.x1, self.y1, self.z1 = tuple(self.p1)

    def intersects(self, x):
        return not ((x < self.x0 and x < self.x1) or (x > self.x0 and x > self.x1))

    def frames_intersected(self):
        if self.x0 < self.x1:
            return list(range(self.x0, self.x1))

        return list(range(self.x1, self.x0))

    def intersection(self, x):
        # There are no intersections if the plane with equation X=x 
        # is outside of the line segment
        if not self.intersects(x):
            return []
        
        # The two endpoints are intersection points if they reside on the plane
        if (self.x1 == self.x0 and self.x0 == x):
            return [[self.x0, self.y0, self.z0], [self.x1, self.y1, self.z1]]

        # Compute the intersection point
        t = (x - self.x0) / (self.x1 - self.x0)
        y = self.y0 + t * (self.y1 - self.y0)
        z = self.z0 + t * (self.z1 - self.z0)

        # Build the intersection point
        return [[round(x), round(y), round(z)]]