import cv2, time


class SpeedTracker:
    def __init__(self):
        self.start_time = None
        self.fps = None
        self.frame_count = 0.0

    def start(self):
        self.start_time = time.time()

    def count_frame(self):
        self.frame_count += 1.0
        self.fps = self.frame_count / (time.time() - self.start_time)

    def get_speed(self, deque):
        if len(deque) > 1:
            (x1, x2) = (deque[0], deque[1])
            if x1 is not None and x2 is not None:
                distance = (x1[0] - x2[0]) ** 2.0 + (x1[1] - x2[1]) ** 2.0
                return distance / self.fps
            else:
                return 0.0
        else:
            return 0.0

    def print_fps(self, scene, position=None):
        position = position or (10, 50)
        cv2.putText(scene, "fps: " + str(self.fps), position,
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def print_speed(self, scene, deque, idx, position=None):
        position = position or (10, scene.shape[0] - 50 - 30 * idx)
        cv2.putText(scene, "speed: " + str(self.get_speed(deque)) + " px/s",
                    position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
