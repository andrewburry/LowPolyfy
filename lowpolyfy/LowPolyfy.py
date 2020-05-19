import logging
from cv2 import VideoCapture, VideoWriter, VideoWriter_fourcc, imshow
from lowpolyfy.utils.video_utils import video_exists, get_video_parameters
from lowpolyfy.VideoCube import VideoCube
from lowpolyfy.pointplacement.PointPlacer import PointPlacer

logger = logging.getLogger(__name__)

class LowPolyfy():

    def _initialize_point_placer(self, algorithm, video_cube, num_points):
        # Create the point placer
        logger.info("Creating the point placer object.")
        placer = PointPlacer()

        # Set the point placement algorithm
        logger.info("Setting the placement algorithm to be {}.".format(algorithm))
        algorithm_set = placer.set_algorithm(algorithm)
        if not algorithm_set:
            # Signify initialization failed
            return False

        # Place points within the video cube
        placer.place_points(video_cube, num_points)
        return True

    def approximate(self, source_path, algorithm, num_points):
        # Check to ensure that a file exists at the specified path
        if (not video_exists(source_path)):
            logger.error("Failed to find a video file at the specified path.")
            return

        # Setting up video reader
        video = VideoCapture(source_path)

        # Find the dimensions of the video to define the video cube
        num_frames, video_width, video_height, fps = get_video_parameters(video)
        vc = VideoCube(num_frames, video_height, video_width)

        # Setting up video writer
        fourcc = VideoWriter_fourcc(*'DIVX')
        video_out = VideoWriter("output.mp4", fourcc, fps, (video_width, video_height))
        
        # Initialize the video cube according to the point initialization algorithm
        # Exit if points failed to be placed
        if not self._initialize_point_placer(algorithm, vc, num_points):
            logger.error("Point placement failed to initialize.")
            return

        # Tetrahedralize the video cube
        vc.tetrahedralize()

        # Loop through the 
        frame_number = 0
        while video.isOpened():
            # Read a frame of the video
            frames_remain, frame = video.read()

            # Stop reading if we reach the end of the video
            if not frames_remain:
                break

            # Slice the video cube at this frame and create a low poly frame
            frame_lp = vc.slice_cube(frame, frame_number)
            frame_number += 1

            # Write the low poly frame
            video_out.write(frame_lp)

        # Release video reader and writer
        video_out.release()
        video.release()
        

