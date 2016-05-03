import argparse

import cv2

from utils.utils import do_track_with


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-v", "--video", help="path to the (optional) video file")
args_parser.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(args_parser.parse_args())

# colors ranges in format [lower_bound, upper_bound]
green_color_range = [(29, 86, 6), (64, 255, 255)]
red_color_range = [(0, 195, 205), (255, 255, 255)]
colors = [green_color_range, red_color_range]
max_buffer_length = args["buffer"]

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

do_track_with(title="Hand tracking", camera=camera, colors=colors, max_buffer_size=max_buffer_length)
camera.release()
cv2.destroyAllWindows()
