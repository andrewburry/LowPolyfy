from os import path
from cv2 import CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FPS

def video_exists(file_path):
    # TODO: ensure path exists and it has a video format

    return path.exists(file_path)

def get_video_parameters(video):
    length = int(video.get(CAP_PROP_FRAME_COUNT))
    height = int(video.get(CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(CAP_PROP_FRAME_WIDTH))
    fps = int(video.get(CAP_PROP_FPS))

    return (length, height, width, fps)
