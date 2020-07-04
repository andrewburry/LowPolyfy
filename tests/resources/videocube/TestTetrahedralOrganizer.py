import unittest
from random import randint
from numpy import empty
from lowpolyfy.resources.videocube.TetrahedralOrganizer import TetrahedralOrganizer
from lowpolyfy.resources.geometry.Tetrahedral import Tetrahedral

class TestTetrahedralOrganizer(unittest.TestCase):

    def _create_tetrahedrals(self, numTetrahedrals, numFrames):
        tetrahedrals = []
        expectedBinSizes = self.bins = list(empty(numFrames))
        for i in range(numTetrahedrals):
            # Generate 4 points
            p0 = (randint(0, numFrames - 1), randint(0, numFrames - 1), randint(0, numFrames - 1))
            p1 = (randint(0, numFrames - 1), randint(0, numFrames - 1), randint(0, numFrames - 1))
            p2 = (randint(0, numFrames - 1), randint(0, numFrames - 1), randint(0, numFrames - 1))
            p3 = (randint(0, numFrames - 1), randint(0, numFrames - 1), randint(0, numFrames - 1))

            tetrahedral = Tetrahedral([p0, p1, p2, p3])
            framesIntersected = tetrahedral.frames_intersected()

            for frame in framesIntersected:
                expectedBinSizes[frame] += 1

            tetrahedrals.append(tetrahedral)
        return (tetrahedrals, expectedBinSizes)


    def test_insert(self):
        numFrames = 10
        numTetrahedrals = 10

        organizer = TetrahedralOrganizer(numFrames)

        # Generate random tetrahedrals
        tetrahedrals, expectedBinSizes = self._create_tetrahedrals(numTetrahedrals, numFrames)
        
        # Place them in the organizer
        organizer.insert(tetrahedrals)

        for i in range(numFrames):
            self.assertEqual(len(organizer.bins[i]), expectedBinSizes[i])


if __name__ == '__main__':
    unittest.main()