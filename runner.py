# import the necessary packages
from collections import deque
import argparse

import cv2

from utils.utils import track_color


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green" ball in the HSV color space, then initialize the
# list of tracked points
green_color_range = [(29, 86, 6), (64, 255, 255)]
red_color_range = [(0, 195, 205), (255, 255, 255)]
colors = [green_color_range, red_color_range]
max_buffer_length = args["buffer"]
pts = deque(maxlen=max_buffer_length)

# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

track_color(camera=camera, pts=pts, colors=colors, max_buffer_size=max_buffer_length)

camera.release()
cv2.destroyAllWindows()
