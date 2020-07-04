import unittest
from random import randint
from lowpolyfy.resources.pointplacement.box.v2.SubdividingBox import SubdividingBox

class TestSubdividingBox(unittest.TestCase):

    def setUp(self):
        origin = (0,0,0)
        self.dimension = (10, 10, 10)
        self.threshold = 2
        self.box = SubdividingBox(origin, self.dimension, self.threshold)

    def _generate_random_point(self):
        return (randint(0, 9), randint(0, 9), randint(0, 9))

    def test_dimension_check(self):
        # Case 1: Can be placed in
        self.assertFalse(self.box._dimension_check((20, 20, 20)))

        # Case 2: Cannot be placed in
        self.assertTrue(self.box._dimension_check((5, 5, 5)))
    
    def test_insert(self):
        # Ensure the box is empty first
        self.assertFalse(self.box.boxes)

        # Case 1: Box does not subdivide on insert
        self.assertTrue(self.box.insert(self._generate_random_point()))
        self.assertFalse(self.box.boxes)

        # Case 2: Box subdivides on insert
        self.assertTrue(self.box.insert(self._generate_random_point()))
        self.assertTrue(self.box.boxes)







if __name__ == '__main__':
    unittest.main()