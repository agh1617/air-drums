from collections import deque
from speed_tracker import SpeedTracker
from drum import Drum
from utils import *

import cv2
import imutils
import numpy as np


def track_stick_position(frame, hsv, colors, min_radius):
    lower_color_bounds = colors[0]
    upper_color_bounds = colors[1]

    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype="uint8")

    for i in xrange(0, len(lower_color_bounds)):
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower_color_bounds[i], upper_color_bounds[i]))

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    stick_position = None
    if len(contours) > 0:
        centroid = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(centroid)
        m = cv2.moments(centroid)
        stick_position = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))

    return stick_position


def preprocess_frame(frame):
    resized = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(resized, (11, 11), 0)
    hsv     = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    return resized, hsv


def track_sticks(camera, colors, min_radius=10, video_mode=False, title=None):
    num_sticks = len(colors)

    stick_positions = [deque(maxlen=2) for _ in xrange(num_sticks)]

    drums_scene = cv2.imread('graphics/drums_set.png')

    drums = [
        Drum(((590, 265), (735, 365)), 'samples/drum1.wav'),
        Drum(((275, 75),  (440, 170)), 'samples/drum2.wav'),
        Drum(((600, 75),  (765, 165)), 'samples/drum3.wav'),
        Drum(((385, 270), (520, 390)), 'samples/drum4.wav')
    ]

    drums_scene_dim = drums_scene.shape
    frame_dim = frame_shape(camera)

    def normalize_stick_position((x, y)):
        return (int(x / frame_dim[0] * drums_scene_dim[1]), int(y / frame_dim[1] * drums_scene_dim[0]))

    def color_speed_position(stick_num):
        return (12, drums_scene_dim[0] - 42 - 30 * stick_num)

    speed_tracker = SpeedTracker()
    speed_tracker.start()

    while True:
        current_scene = drums_scene.copy()

        (grabbed, frame) = camera.read()
        frame = cv2.flip(frame, 1)

        if video_mode and not grabbed:
            break

        frame, hsv = preprocess_frame(frame)
        
        speed_tracker.count_frame()
        speed_tracker.print_fps(frame)

        map(lambda drum: drum.draw(current_scene), drums)

        for stick_num in xrange(num_sticks):
            color = colors[stick_num]

            prev_positions = stick_positions[stick_num]
            curr_position  = track_stick_position(frame, hsv, colors=color, min_radius=min_radius)

            if curr_position:
                normalized_position = normalize_stick_position(curr_position)
                prev_positions.appendleft(normalized_position)

                cv2.circle(current_scene, normalized_position, 5, color[2], -1)

                map(lambda drum: drum.play(normalized_position, speed_tracker.get_speed(prev_positions)), drums)

            speed_position = color_speed_position(stick_num)
            speed_tracker.print_speed(current_scene, prev_positions, position=speed_position)

        cv2.imshow(title, current_scene)

        if key_pressed("q"):
            break

    camera.release()
