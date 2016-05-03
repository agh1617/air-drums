from collections import deque
from speed_tracker import SpeedTracker

import cv2
import imutils
import numpy as np


def key_pressed(key_string):
    key = cv2.waitKey(1) & 0xFF
    return key == ord(key_string)


def track_single_color(frame, hsv, tracked_points, colors, points_buffer_size, min_radius):
    lower_color_bound = colors[0]
    upper_color_bound = colors[1]
    draw_color = colors[2]
    # construct a mask for the color "green", then perform a series of dilations and erosions
    # to remove any small blobs left in the mask
    mask = cv2.inRange(hsv, lower_color_bound, upper_color_bound)
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

        # only proceed if the radius meets a minimum size
        if radius > min_radius:
            # draw the circle and centroid on the frame, then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), draw_color, 2)
            cv2.circle(frame, center, 5, draw_color, -1)

    tracked_points.appendleft(center)
    for points_index in xrange(1, len(tracked_points)):
        # if either of the tracked points are None, ignore them
        if tracked_points[points_index - 1] is None or tracked_points[points_index] is None:
            continue

        # otherwise, compute the thickness of the line and draw the connecting lines
        thickness = int(np.sqrt(points_buffer_size / float(points_index + 1)) * 2.5)
        cv2.line(frame, tracked_points[points_index - 1], tracked_points[points_index], draw_color, thickness)


def do_track_with(title, camera, colors, points_buffer_size, min_radius=10, video_mode=False):
    colors_length = len(colors)
    points_list = [deque(maxlen=points_buffer_size) for _ in xrange(colors_length)]
    speed_tracker = SpeedTracker()
    speed_tracker.start()

    while True:
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

        for color_index in xrange(colors_length):
            current_color = colors[color_index]
            points = points_list[color_index]
            track_single_color(frame, hsv, points,
                               colors=current_color,
                               points_buffer_size=points_buffer_size,
                               min_radius=min_radius)

            speed_position = (12, frame.shape[0] - 42 - 30 * color_index)
            speed_tracker.print_speed(frame, points, position=speed_position)


        cv2.imshow(title, frame)
        if key_pressed("q"):
            break

    camera.release()
