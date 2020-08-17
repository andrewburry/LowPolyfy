import logging
from numpy import array
from scipy.spatial import Delaunay
from numpy import zeros, int32, uint8
from cv2 import fillPoly, polylines, circle, mean
from lowpolyfy.resources.geometry.Tetrahedral import Tetrahedral
from lowpolyfy.resources.videocube.TetrahedralOrganizer import TetrahedralOrganizer

logger = logging.getLogger(__name__)

class VideoCube():
    def __init__(self, num_frames, width, height):
        # Retain the dimensions of the video cube
        self.num_frames = num_frames
        self.dimensions = (num_frames, width, height)
        self.height = height
        self.width = width

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
        self._mask = zeros([height, width], uint8)
        self._organizer = TetrahedralOrganizer(num_frames)

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
            corners = []
            for index in simplex:
                corners.append(self._points[index])
            self._tetrahedrals.append(Tetrahedral(corners))

        self._organizer.insert(self._tetrahedrals)

        logger.info("Created {} tetrahedrals in the video cube".format(len(self._tetrahedrals)))
        return

    def _remove_temporal_dimension(self, polygon):
        # Discard the time dimension
        frame_polygons = []
        for point in polygon:
            frame_polygons.append([point[1], point[2]])

        # Filling polygons of dimensions n=1,2,3 are point order independent.
        # For the case where there are four intersection points, we have to
        # reorder two points. The cv2 fillpoly method plots points in order
        # and fills the resulting polygon. We will only ever have n=1,2,3,4 ngons.
        if len(frame_polygons) == 4:
            tmp = frame_polygons[2]
            frame_polygons[2] = frame_polygons[3]
            frame_polygons[3] = tmp
        
        return frame_polygons

    def slice_cube(self, frame, frame_number):
        # Now that I have converted each of the simplices, 
        # I can now start walking the video cube temporally
        logger.info("Processing frame number {}/{}.".format(frame_number + 1, self.num_frames))

        # TODO: bring this out to reduce time
        polygons = []
        frame_tets = self._organizer.bins[frame_number]

        # Find the intersection of the frame and the tetrahedrals
        for tetrahedral in frame_tets:
            pnts = tetrahedral.intersection(frame_number)
            logger.debug("Found {} intersection points for tetrahedral {}".format(len(pnts), tetrahedral))
            if len(pnts) >= 2:
                polygons.append(pnts)
        
        logger.info("Drawing {} polygons on the low-poly frame.".format(len(polygons)))
        lp_frame = frame.copy()
        lp_frame_lines = frame.copy()
        lp_frame_points = frame.copy()
        lp_frame_key_points = frame.copy()

        # Found out that finding the average color of each polygon takes a considerable amount of time
        # Consider methods to speed up computation here
        for polygon in polygons:
            self._process_polygon(polygon, frame, lp_frame, lp_frame_lines, lp_frame_points)
        
        lp_frame_key_points = self._draw_key_points(lp_frame_key_points, frame_number)
            
        logger.info("Created low-poly frame.")
        return (lp_frame, lp_frame_lines, lp_frame_points, lp_frame_key_points)

    def _find_average_color(self, polygon, frame):
        r, g, b = (0, 0, 0)
        numPoints = len(polygon)
        for x, y in polygon:
            # Find the corresponding pixel
            _r, _g, _b = tuple(list(frame[y - 1][x - 1]))

            r += _r
            g += _g
            b += _b

        return (round(r/numPoints), round(g/numPoints), round(b/numPoints))

    def _find_centroid_color(self, polygon, frame):
        c_x = 0
        c_y = 0
        # Average the x, and y values of the polygon points
        for x, y in polygon:
            c_x += x
            c_y += y

        c_x = round(c_x/len(polygon))
        c_y = round(c_y/len(polygon))

        # Extract the frame data at the centroid location
        r, g, b = tuple(list(frame[y - 1][x - 1]))

        # Convert the int64 datatypes to int
        return (int(r), int(g), int(b))
            

    def _process_polygon(self, polygon, frame, lp_frame, lp_frame_lines, lp_frame_points):
        polygon = self._remove_temporal_dimension(polygon)
        mask = zeros([self.height, self.width], uint8)
        fillPoly(mask, array([polygon]), 255)
        r, g, b, _ = [round(_) for _ in mean(frame, mask=mask)]
        #r, g, b = self._find_average_color(polygon, frame)
        fillPoly(lp_frame, pts=array([polygon]), color=(r, g, b))

        # Line view
        # Draw the polygon lines on line view
        polylines(lp_frame_lines, pts=array([polygon]), isClosed=True, color=(0, 0, 0))

        for point in polygon:
            circle(lp_frame_points, tuple(point), 2, (0, 0, 0))

    def _draw_key_points(self, lp_frame, frame_number):
        
        # Find points on this frame number and remove the temporal dimension
        for point in self._points:
            if point[0] == frame_number:
                circle(lp_frame, (point[1], point[2]), 10, (0,0,0))

        return lp_frame

