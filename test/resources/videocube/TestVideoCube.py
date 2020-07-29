import unittest
from random import randint
from numpy import empty
from lowpolyfy.resources.videocube.VideoCube import VideoCube
from lowpolyfy.resources.geometry.Tetrahedral import Tetrahedral

class test_videocube(unittest.TestCase):
    def test_find_centroid_color(self, polygon, frame):
        x=0
        vc = VideoCube(1, 100, 100)

        

        r, g, b = vc._find_centroid_color(polygon, frame)