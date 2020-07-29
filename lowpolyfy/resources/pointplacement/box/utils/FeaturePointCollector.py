from cv2 import goodFeaturesToTrack, CAP_PROP_POS_FRAMES, cvtColor, COLOR_BGR2GRAY, medianBlur


class FeaturePointCollector():
    def __init__(self):
        self.maxCorners = 1000 # 1000
        self.qualityLevel = 0.00001
        self.minDistance = 1 #10
        
    def generate_keypoints_from_features(self, video):
        points = []

        # Loop through the 
        frame_number = 0
        while video.isOpened():
            # Read a frame of the video
            frames_remain, frame = video.read()

            # Stop reading if we reach the end of the video
            if not frames_remain:
                break
            
            gray = cvtColor(frame, COLOR_BGR2GRAY)

            blurred = medianBlur(gray, 5)

            discovered_points = goodFeaturesToTrack(blurred, self.maxCorners, self.qualityLevel, self.minDistance)
            for point in discovered_points:
                y, x = point.ravel()
                points.append([frame_number, int(y), int(x)])

            frame_number += 1
    
        # Reset the video capture to frame 0
        video.set(CAP_PROP_POS_FRAMES, 0)
        return points