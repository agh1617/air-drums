from collections import deque
from speed_tracker import SpeedTracker
from drum import Drum
from utils import *

import cv2
import imutils
import numpy as np


def track_single_color(frame, scene, hsv, tracked_points, colors, points_buffer_size, min_radius):
    lower_color_bounds = colors[0]
    upper_color_bounds = colors[1]
    draw_color = colors[2]

    # construct a mask for the color "green", then perform a series of dilations and erosions
    # to remove any small blobs left in the mask
    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype="uint8")
    for i in xrange(0, len(lower_color_bounds)):
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower_color_bounds[i], upper_color_bounds[i]))

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current (x, y) center of the ball
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    center = None
    if len(contours) > 0:
        # find the largest contour in the mask, then use it to compute the minimum
        # enclosing circle and centroid
        centroid = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(centroid)
        m = cv2.moments(centroid)
        center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))

    tracked_points.appendleft(center)

    return center


def do_track_with(title, camera, colors, points_buffer_size, min_radius=10, video_mode=False):
    colors_length = len(colors)
    points_list = [deque(maxlen=points_buffer_size) for _ in xrange(colors_length)]
    speed_tracker = SpeedTracker()
    speed_tracker.start()

    drums_scene = cv2.imread('graphics/drums_set.png')
    drums_scene_dim = drums_scene.shape

    frame_dim = frame_shape(camera)

    def normalize_stick_position((x, y)):
        return (int(x / frame_dim[0] * drums_scene_dim[1]), int(y / frame_dim[1] * drums_scene_dim[0]))

    def color_speed_position(color_index):
        return (12, drums_scene_dim[0] - 42 - 30 * color_index)

    drums = []
    drums.append(Drum(((590, 265), (735, 365)), 'samples/drum1.wav'))
    drums.append(Drum(((275, 75), (440, 170)), 'samples/drum2.wav'))
    drums.append(Drum(((600, 75), (765, 165)), 'samples/drum3.wav'))
    drums.append(Drum(((385, 270), (520, 390)), 'samples/drum4.wav'))

    while True:
        current_scene = drums_scene.copy()

        (grabbed, frame) = camera.read()
        frame = cv2.flip(frame, 1)
        speed_tracker.count_frame()
        speed_tracker.print_fps(frame)

        if video_mode and not grabbed:
            break

        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        map(lambda drum: drum.draw(current_scene), drums)

        for color_index in xrange(colors_length):
            current_color = colors[color_index]
            points = points_list[color_index]
            center = track_single_color(frame, current_scene, hsv, points,
                                        colors=current_color,
                                        points_buffer_size=points_buffer_size,
                                        min_radius=min_radius)

            if center:
                normalized_center = normalize_stick_position(center)
                cv2.circle(current_scene, normalized_center, 5, current_color[2], -1)
                map(lambda drum: drum.play(normalized_center, speed_tracker.get_speed(points)), drums)

            speed_position = color_speed_position(color_index)
            speed_tracker.print_speed(current_scene, points, position=speed_position)

        cv2.imshow(title, current_scene)
        if key_pressed("q"):
            break

    camera.release()
