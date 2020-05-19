import logging
from scipy.spatial import Delaunay
from numpy import zeros, int32, uint8
from cv2 import fillPoly, mean
from lowpolyfy.utils.slice_utils import find_tetrahedral_frame_intersections

logger = logging.getLogger(__name__)

class VideoCube():
    def __init__(self, num_frames, width, height):
        # Retain the dimensions of the video cube
        self.num_frames = num_frames
        self.dimensions = (num_frames, width, height)

        # Store the corners of the video cube
        self._points = [
            [0, 0, 0],
            [0, 0, height],
            [0, width, 0],
            [0, width, height],
            [num_frames, 0, 0],
            [num_frames, 0, height],
            [num_frames, width, 0],
            [num_frames, width, height]
        ]

    def add_points(self, points):
        self._points += points
        return

    def tetrahedralize(self):
        logger.info("Performing tetrahedralization on the video cube.")
        simplices = Delaunay(self._points).simplices
        
        # Simplices are indices of each triangle vertex
        # Convert indices to points
        self._tetrahedrals = []
        for simplex in simplices:
            point = []
            for index in simplex:
                point.append(self._points[index])
            self._tetrahedrals.append(point)

        # Clean up the points that were placed in the video cube.
        # We are only concerned about the tetrahedrals now.
        del self._points

        logger.info("Created {} tetrahedrals in the video cube".format(len(self._tetrahedrals)))
        return

    def _remove_temporal_dimension(self, polygon):
        # Discard the time dimension
        frame_polygons = []
        for point in polygon:
            frame_polygons.append([point.y, point.z])

        # Filling polygons of dimensions n=1,2,3 are point order independent.
        # For the case where there are four intersection points, we have to
        # reorder two points. The cv2 fillpoly method plots points in order
        # and fills the resulting polygon. We will only ever have n=1,2,3,4 ngons.
        if len(frame_polygons) == 4:
            tmp = frame_polygons[2]
            frame_polygons[2] = frame_polygons[3]
            frame_polygons[3] = tmp
        
        return int32([frame_polygons])

    def slice_cube(self, frame, frame_number):
        # Now that I have converted each of the simplices, 
        # I can now start walking the video cube temporally
        logger.info("Processing frame number {}/{}.".format(frame_number + 1, self.num_frames))

        polygons = []
        # Find the intersection of the frame and the tetrahedrals
        for tetrahedral in self._tetrahedrals:
            pnts = find_tetrahedral_frame_intersections(tetrahedral, frame_number)
            logger.info("Found {} intersection points for tetrahedral {}".format(len(pnts), tetrahedral))
            if pnts:
                polygons.append(pnts)
        
        logger.info("Drawing polygons on the low-poly frame.")
        lp_frame = frame.copy()
        for polygon in polygons:
            # Reduce the dimensionality of the polygon. We know the intersection 
            # is for this frame number 
            polygon = self._remove_temporal_dimension(polygon)

            # Create a mask with the polygon
            mask = zeros(frame.shape[:2], uint8)
            fillPoly(mask, pts=polygon, color=(255,255,255))
            
            # Fetch the average color in within the mask
            r, g, b, _ = [int(_) for _ in mean(frame, mask=mask)]

            # Fill the polygon on the lp frame with the average color of the mask
            fillPoly(lp_frame, pts=polygon, color=(r,g,b))

        logger.info("Created low-poly frame.")
        return lp_frame
