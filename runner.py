import argparse

import cv2

from tracking.tracking import do_track_with


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-v", "--video", help="path to the (optional) video file")
args_parser.add_argument("-b", "--buffer", type=int, default=64, help="points buffer size")
args = vars(args_parser.parse_args())

# colors ranges in format [lower_bound - hsv, upper_bound - hsv, draw_color - rgb]
green_color_range = [(29, 86, 6), (64, 255, 255), (0, 255, 0)]
red_color_range = [(0, 195, 205), (255, 255, 255), (255, 0, 0)]
colors = [green_color_range, red_color_range]
points_buffer_size = args["buffer"]

local_camera_mode = not args.get("video", False)
camera = cv2.VideoCapture(0) if local_camera_mode else cv2.VideoCapture(args["video"])

do_track_with(title="Hand tracking", camera=camera, colors=colors, points_buffer_size=points_buffer_size)
camera.release()
cv2.destroyAllWindows()
