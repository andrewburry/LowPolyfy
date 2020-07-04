import unittest
from lowpolyfy.resources.geometry.LineSegment import LineSegment

class test_linesegment(unittest.TestCase):

    def test_intersects(self):
        p0 = (1, 1, 1)
        p1 = (2, 2, 2)

        lineSegment = LineSegment(p0, p1)

        # Case 1: Previous frame
        self.assertFalse(lineSegment.intersects(0))

        # Case 2: Frame after
        self.assertFalse(lineSegment.intersects(3))

        # Case 3: Frame within line
        self.assertTrue(lineSegment.intersects(2))

        # Both p0 and p1 lie on the same point
        lineSegment = LineSegment(p0, p0)

        # Case 4: Previous frame
        self.assertFalse(lineSegment.intersects(0))

        # Case 5: Frame after
        self.assertFalse(lineSegment.intersects(2))

        # Case 6: Frame within line
        self.assertTrue(lineSegment.intersects(1))

        # Case 7: Frame None type
        self.assertRaises(TypeError, lineSegment.intersects, None)

    def test_frames_intersected(self):
        p0 = (1, 1, 1)
        p1 = (2, 2, 2)

        lineSegment = LineSegment(p0, p1)

        # Case 1: Increasing order of p0 and p1
        expectation = [1, 2]
        found = lineSegment.frames_intersected()
        self.assertEqual(found, expectation)

        # Case 2: Decreasing order of p0 and p1
        lineSegment = LineSegment(p1, p0)
        found = lineSegment.frames_intersected()
        self.assertEqual(found, expectation)

        # Case 3: Same point
        expectation = [1]
        lineSegment = LineSegment(p0, p0)
        found = lineSegment.frames_intersected()
        self.assertEqual(found, expectation)

    def test_intersection(self):
        p0 = (1, 1, 1)
        p1 = (3, 3, 3)

        lineSegment = LineSegment(p0, p1)

        # Case 1: plane is out of bounds
        self.assertFalse(lineSegment.intersection(0))
        self.assertFalse(lineSegment.intersection(4))

        # Case 2: Intersection is on an endpoint
        self.assertEqual([list(p0)], lineSegment.intersection(1))
        self.assertEqual([list(p1)], lineSegment.intersection(3))

        # Case 3: Intersection is some where between the endpoints
        self.assertEqual([[2, 2, 2]], lineSegment.intersection(2))

        # Case 4: Intersection contains both endpoints
        p0 = (1, 1, 1)
        p1 = (1, 2, 2)

        lineSegment = LineSegment(p0, p1)
        self.assertEqual([list(p0), list(p1)], lineSegment.intersection(1))

        # Case 5: Calculated intersection is rounded: 1.5 -> up
        p0 = (1, 1, 1)
        p1 = (2, 2, 2)

        lineSegment = LineSegment(p0, p1)
        self.assertEqual([[2, 2, 2]], lineSegment.intersection(1.5))

        # Case 6: Calculated intersection is rounded down 1.49 -> down
        self.assertEqual([[1, 1, 1]], lineSegment.intersection(1.49))

if __name__ == '__main__':
    unittest.main()
