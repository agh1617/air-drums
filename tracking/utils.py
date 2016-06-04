import cv2


def frame_shape(camera):
    return camera.get(3), camera.get(4)


def key_pressed(key_string):
    key = cv2.waitKey(1) & 0xFF
    return key == ord(key_string)
