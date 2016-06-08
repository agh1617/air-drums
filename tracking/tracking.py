import cv2, imutils
import numpy as np

from speed_tracker import SpeedTracker
from drum import Drum
from utils import frame_shape, key_pressed


def track_stick_position(frame, hsv, stick):
    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype="uint8")

    # construct a mask for the stick color
    mask = cv2.inRange(
        hsv,
        stick.lower_color_bounds,
        stick.upper_color_bounds
    )

    # perform a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask
    contours = cv2.findContours(
        mask.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    contours = contours[-2]

    stick_position = None

    # find the largest contour in the mask, then use
	# it to compute the centroid of stick's position
    if len(contours) > 0:
        centroid = max(contours, key=cv2.contourArea)
        centroid_moments = cv2.moments(centroid)

        stick_position = (
            int(centroid_moments["m10"] / centroid_moments["m00"]),
            int(centroid_moments["m01"] / centroid_moments["m00"])
        )

    return stick_position


def preprocess_frame(frame):
    # resize the frame - allows to process the frame faster,
    # leading to an increase in FPS
    resized = imutils.resize(frame, width=600)

    # blur the frame - reduces high frequency noise,
    # allowing to focus on the structural objects inside the
    blurred = cv2.GaussianBlur(resized, (11, 11), 0)

    # convert frame to HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    return resized, hsv


def build_preview(frame, size=300):
    frame_preview = frame.copy()
    frame_preview = imutils.resize(frame_preview, width=size)
    preview_dim = frame_preview.shape
    return frame_preview, preview_dim


def track_sticks(camera, sticks, video_mode=False, debug_mode=False, title=None):
    drums_scene = cv2.imread('graphics/drums_set.png')

    drums = [
        Drum(((590, 265), (735, 365)), 'samples/drumset_2/tom.wav'),
        Drum(((275, 75),  (440, 170)), 'samples/drumset_2/crash_1.wav'),
        Drum(((600, 75),  (765, 165)), 'samples/drumset_2/crash_2.wav'),
        Drum(((385, 270), (520, 390)), 'samples/drumset_2/snare.wav')
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

        if debug_mode:
            speed_tracker.print_fps(current_scene)

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

            if debug_mode:
                speed_tracker.print_speed(
                    current_scene,
                    stick.positions,
                    idx
                )

        # build frame preview, paste it in bottom-right corner of scene
        frame_preview, preview_dim = build_preview(frame)

        current_scene[
            (drums_scene_dim[0] - preview_dim[0] - 20):(drums_scene_dim[0] - 20),
            (drums_scene_dim[1] - preview_dim[1] - 20):(drums_scene_dim[1] - 20)
        ] = frame_preview

        cv2.imshow(title, current_scene)

        if key_pressed("q"):
            break

    camera.release()
