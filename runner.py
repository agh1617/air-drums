import argparse
import cv2
from tracking.tracking import track_sticks
from tracking.stick import Stick


args_parser = argparse.ArgumentParser()
args_parser.add_argument("-v", "--video", help="path to the (optional) video file")
args_parser.add_argument("-d", "--debug", help="enable debug mode", action='store_true')
args = vars(args_parser.parse_args())

# colors ranges in format (lower_bound - hsv, upper_bound - hsv, draw_color - bgr)
sticks = [
    Stick(((95, 180, 50), (255, 255, 255), (0, 255, 0))),  # blue
    Stick(((113, 56, 164), (141, 255, 255), (0, 0, 250)))  # purple
]

video_mode = not args.get("video", False)
debug_mode = args.get("debug", False)

camera = cv2.VideoCapture(0) if video_mode else cv2.VideoCapture(args["video"])

track_sticks(camera, sticks, video_mode=video_mode, debug_mode=debug_mode, title="Air drums")

camera.release()
cv2.destroyAllWindows()
