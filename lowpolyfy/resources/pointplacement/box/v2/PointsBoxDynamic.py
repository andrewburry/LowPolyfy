import logging
from lowpolyfy.resources.pointplacement.box.v2.SubdividingBox import SubdividingBox
from lowpolyfy.resources.pointplacement.box.utils.FeaturePointCollector import FeaturePointCollector
from lowpolyfy.resources.utils.video_utils import get_video_parameters
from cv2 import CAP_PROP_POS_FRAMES, VideoWriter, VideoWriter_fourcc, fillPoly
from numpy import zeros, uint8, array

logger = logging.getLogger(__name__)

class PointsBoxDynamic():
    def generate_points(self, dimensions, numPoints, video):
        _, self.width, self.height = dimensions

        # Generate points from features in the video
        logger.info("Generating feature points within the video cube of dimensions {}".format(dimensions))
        points = FeaturePointCollector().generate_keypoints_from_features(video)
        logger.info("Generated {} feature points within the video cube of dimensions {}".format(len(points), dimensions))
        
        # Create the box binner
        box = SubdividingBox(origin=(0,0,0), dimensions=dimensions, subdivideThreshold=numPoints, depthThreshold=14, depth=0)

        # Place points into the binner
        logger.info("Inserting {} points into the subdividing box".format(len(points)))

        for point in points:
            box.insert(point)
        
        # Extract the boxes for logging
        allBoxes = box.fetch_all_boxes()
        endpointBoxes = box.fetch_end_point_boxes()
        logger.info("Created {} boxes where {} are endpoint boxes".format(len(allBoxes), len(endpointBoxes)))

        # Extract points from the structure
        points = box.fetch_random_points()
        logger.info("Returning {} points from the subdividing box".format(len(points)))

        # Generate a view
        logger.info("Generating the Spatial Subdivision Box view")
        self.generate_view(endpointBoxes, video)
        logger.info("Generated the Spatial Subdivision Box view")

        return points

    def generate_view(self, endpointBoxes, video):
        # TODO: move this somewhere that makes more sense. Perhaps just the writer setup logic
        points = []

        # Setup the output device
        fourcc = VideoWriter_fourcc(*'mp4v')
        num_frames, video_width, video_height, fps = get_video_parameters(video)
        video_out = VideoWriter("views/output_boxes.mp4", fourcc, fps, (video_height, video_width))

        # Loop through the video
        frame_number = 0
        while video.isOpened():
            # Read a frame of the video
            frames_remain, frame = video.read()

            # Stop reading if we reach the end of the video
            if not frames_remain:
                break
            
            frame_lp = self._slice_frame(endpointBoxes, frame, frame_number)
            
            video_out.write(frame_lp)
            frame_number += 1
    
        # Reset the video capture to frame 0
        video.set(CAP_PROP_POS_FRAMES, 0)
        return

    def _slice_frame(self, endpointBoxes, frame, frameNumber):
        frame_box_view = frame.copy()

        # Extract and draw the boxes on the frame
        for box in endpointBoxes:
            if box.is_visible_on_frame(frameNumber):                
                fillPoly(frame_box_view, pts=array([box.get_polygon()]), color=box.color)

        return frame_box_view

