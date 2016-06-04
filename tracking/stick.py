import cv2
from collections import deque


class Stick:
    def __init__(self, colors):
        self.lower_color_bounds = colors[0]
        self.upper_color_bounds = colors[1]
        self.draw_color = colors[2]

        self.positions = deque(maxlen=2)

    def draw(self, scene):
        cv2.circle(scene, self.positions[0], 5, self.draw_color, -1)
