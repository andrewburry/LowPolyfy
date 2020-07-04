import unittest
from lowpolyfy.resources.geometry.Tetrahedral import Tetrahedral

class test_tetrahedral(unittest.TestCase):
    def test_tetrahedral_initialized(self):
        p0 = [0, 0, 0]
        p1 = [2, 2, 2]
        p2 = [0, 1, 0]
        p3 = [0, 1, 1]

        tetrahedral = Tetrahedral([p0, p1, p2, p3])

        # Case 1: There are 6 line segments within the tetrahedral
        self.assertTrue(len(tetrahedral.lines) == 6)

        # Case 2: No two lines are the same
        self.assertTrue(len(set(tetrahedral.lines)) == 6)

    def test_frames_intersected(self):
        p0 = [0, 0, 0]
        p1 = [2, 2, 2]
        p2 = [0, 1, 0]
        p3 = [0, 1, 1]

        tetrahedral = Tetrahedral([p0, p1, p2, p3])

        # Case 1: Expecting 0, 1, 2 frames to be interesected
        expected = [0, 1, 2]
        self.assertEqual(tetrahedral.frames_intersected(), expected)

    def test_intersection(self):
        p0 = [1, 0, 0]
        p1 = [2, 2, 2]
        p2 = [1, 1, 0]
        p3 = [1, 1, 1]

        tetrahedral = Tetrahedral([p0, p1, p2, p3])

        # Case 1: plane is out of bounds, i.e. 0 points
        self.assertFalse(tetrahedral.intersection(0))
        self.assertFalse(tetrahedral.intersection(3))

        # Case 2: Intersection is on an endpoint i.e. 1 point
        self.assertEqual([list(p1)], tetrahedral.intersection(2))

        # Case 3: Intersection somewhere within the tetrahedral, i.e. 2, 3 or 4 points
        self.assertEqual([[2, 1, 1], [2, 2, 1], [2, 2, 2]], tetrahedral.intersection(1.5))

        # Case 4: Intersection produces 4 points
        p0 = [1, 0, 0]
        p1 = [2, 10, 10]
        p2 = [6, 1, 0]
        p3 = [6, 10, 1]

        tetrahedral = Tetrahedral([p0, p1, p2, p3])
        self.assertTrue(len(tetrahedral.intersection(3)) == 4)

        # Case 5: Intersection produces 2 points
        self.assertTrue(len(tetrahedral.intersection(6)) == 2)


if __name__ == '__main__':
    unittest.main()

