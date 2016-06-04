from collections import deque
from speed_tracker import SpeedTracker
from drum import Drum
from utils import *

import cv2
import imutils
import numpy as np


def track_stick_position(frame, hsv, stick):
    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype="uint8")

    mask = cv2.bitwise_or(
        mask,
        cv2.inRange(
            hsv,
            stick.lower_color_bounds,
            stick.upper_color_bounds
        )
    )

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(
        mask.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    contours = contours[-2]

    stick_position = None

    if len(contours) > 0:
        centroid = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(centroid)
        centroid_moments = cv2.moments(centroid)

        stick_position = (
            int(centroid_moments["m10"] / centroid_moments["m00"]),
            int(centroid_moments["m01"] / centroid_moments["m00"])
        )

    return stick_position


def preprocess_frame(frame):
    resized = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(resized, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    return resized, hsv


def track_sticks(camera, sticks, video_mode=False, title=None):
    drums_scene = cv2.imread('graphics/drums_set.png')

    drums = [
        Drum(((590, 265), (735, 365)), 'samples/drum1.wav'),
        Drum(((275, 75),  (440, 170)), 'samples/drum2.wav'),
        Drum(((600, 75),  (765, 165)), 'samples/drum3.wav'),
        Drum(((385, 270), (520, 390)), 'samples/drum4.wav')
    ]

    map(lambda drum: drum.draw(drums_scene), drums)

    drums_scene_dim = drums_scene.shape
    frame_dim = frame_shape(camera)

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

        for idx, stick in enumerate(sticks):
            stick_position = track_stick_position(frame, hsv, stick)

            if not stick_position:
                continue

            stick_position = (
                int(stick_position[0] / frame_dim[0] * drums_scene_dim[1]),
                int(stick_position[1] / frame_dim[1] * drums_scene_dim[0])
            )

            stick.positions.appendleft(stick_position)
            stick.draw(current_scene)

            stick_speed = speed_tracker.get_speed(stick.positions)

            map(lambda drum: drum.play(stick_position, stick_speed), drums)

            speed_tracker_position = (
                12,
                drums_scene_dim[0] - 42 - 30 * idx
            )

            speed_tracker.print_speed(
                current_scene,
                stick.positions,
                position=speed_tracker_position
            )

        cv2.imshow(title, current_scene)

        if key_pressed("q"):
            break

    camera.release()
