
import numpy as np
from lowpolyfy.resources.pointplacement.TestObject import TestObject
from math import floor, ceil
import logging
from random import uniform


logger = logging.getLogger(__name__)

class BoxBinner():

    def __init__(self, length, width, height, num_bins):
        self.dimensions = (length, width, height)
        self.num_bins = num_bins

        logger.info("Creating a box of dimension {} containing {} bins".format(self.dimensions, num_bins))
        
        # We need to calculate the dimensions of the bins. 
        # They will have the same proportions as the original cube.

        # Calculate the number of elements each will have
        total_elements = length * width * height
        box_elements = total_elements / num_bins
        
        # Find the ratios of the bin
        ratio_lw = length / width
        ratio_lh = length / height
        ratio_hw = height / width

        # Calculate the bin dimensions
        bin_w = (box_elements / (ratio_lw * ratio_hw)) ** (1./3.)
        bin_l = ratio_lw * bin_w
        bin_h = ratio_hw * bin_w
        self.bin_dimensions = (bin_l, bin_w, bin_h)

        logger.info("Bin dimension calculated to be {}".format(self.bin_dimensions))

        # Create an empty list for the bins
        bins = np.zeros((ceil(length/bin_l), ceil(width/bin_w), ceil(height/bin_h)))
        self.bins = bins.tolist()

    def filter_points(self, points):
        length, width, height = self.bin_dimensions
        logger.info("Inserting {} points into the box binner".format(len(points)))
        for point in points:
            x, y, z = tuple(point)
            # We have a point [l, w, h], and now must find the bin to look in
            index = (floor(x/length), floor(y/width), floor(z/height))

            # Look inside the bin at this index, and insert the point
            i, j, k = index
            self.bins[i][j][k] = point

        points = self._fetch_filtered_points()
        logger.info("Returning {} points from the box binner".format(len(points)))

        return points

    def _fetch_filtered_points(self):
        # Fetch the dimensions of the box, bin and datastructure
        box_l, box_w, box_h = self.dimensions
        bin_l, bin_w, bin_h = self.bin_dimensions
        l,     w,     h     = round(box_l/bin_l), round(box_w/bin_w), round(box_h/bin_h)

        points = []
        # Iterate through the indices of the box datastructure and collect the elements
        for i in range(l):
            for j in range(w):
                for k in range(h):
                    entry = self.bins[i][j][k]

                    # Generate an arbitrary point for the bins that were never modified
                    # Note: we still have the requirement of num_bins number of bins
                    if (type(entry) is not list):
                        entry = self._generate_point(tuple([i, j, k]))

                    points.append(entry)
        
        return points

    def _generate_point(self, index):
        i, j, k = index
        bin_l, bin_w, bin_h = self.bin_dimensions

        lower_l = bin_l * i
        lower_w = bin_w * j
        lower_h = bin_h * k

        l = uniform(lower_l, lower_l + bin_l)
        w = uniform(lower_w, lower_w + bin_w)
        h = uniform(lower_h, lower_h + bin_h)

        return [round(l), round(w), round(h)]


        
