import cv2
from pygame import mixer

mixer.init(frequency=22050, size=-16, channels=2, buffer=8192)

class Drum:
    def __init__(self, rectangle, sound_path, color=(0, 255, 0)):
        self.rectangle = rectangle
        self.color = color
        self.active = False
        self.sound = mixer.Sound(sound_path)

    def draw(self, frame):
        cv2.rectangle(frame, self.rectangle[0], self.rectangle[1], self.color)

    def play(self, center, speed):
        if self.is_played(center):
            volume = min(speed / 200., 1)
            self.sound.set_volume(volume)
            self.sound.play()

    def is_played(self, center):
        if self.rectangle[0][0] < center[0] < self.rectangle[1][0] and self.rectangle[0][1] < center[1] < self.rectangle[1][1]:
            if not self.active:
                self.active = True
                return True
        elif self.active:
            self.active = False
        return False
