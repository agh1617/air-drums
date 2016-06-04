import argparse

import cv2

from tracking.tracking import track_sticks


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(args_parser.parse_args())

# colors ranges in format [lower_bound - hsv, upper_bound - hsv, draw_color - bgr]
green_color_range = [[(45, 80, 80)], [(80, 255, 255)], (0, 255, 0)]
red_color_range = [[(0, 80, 80), (170, 80, 80)], [(10, 255, 255), (180, 255, 255)], (0, 0, 255)]
colors = [green_color_range, red_color_range]

local_camera_mode = not args.get("video", False)
camera = cv2.VideoCapture(0) if local_camera_mode else cv2.VideoCapture(args["video"])

track_sticks(camera=camera, colors=colors, title="Air drums")
camera.release()
cv2.destroyAllWindows()
