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

    def print_fps(self, frame, position=None):
        position = position or (12, frame.shape[0] - 12)
        cv2.putText(frame, "fps: " + str(self.fps), position,
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def print_speed(self, frame, deque, position=None):
        position = position or (12, frame.shape[0] - 42)
        cv2.putText(frame, "speed: " + str(self.get_speed(deque)) + " px/s",
                    position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
