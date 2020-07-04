import unittest
from lowpolyfy.resources.pointplacement.box.v1.BoxBinner import BoxBinner

class TestBoxBinner(unittest.TestCase):

    def test_initialize(self):
        binner = BoxBinner(10, 10, 10, 1000)

        self.assertTrue(binner.binDimensions == (1.0, 1.0, 1.0))

if __name__ == '__main__':
    unittest.main()