class LineSegment():
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
    
    def intersection(self, x):
        x0, y0, z0 = tuple(self.p0)
        x1, y1, z1 = tuple(self.p1)
        # There are no intersections if the plane with equation X=x 
        # is outside of the line segment
        if (x < x0 and x < x1) or (x > x0 and x > x1):
            return []
        
        # The two endpoints are intersection points if they reside on the plane
        if (x1 == x0 and x0 == x):
            return [[x0, y0, z0], [x1, y1, z1]]

        # Compute the intersection point
        t = (x - x0) / (x1 - x0)
        y = y0 + t * (y1 - y0)
        z = z0 + t * (z1 - z0)

        # Build the intersection point
        return [[round(x), round(y), round(z)]]