import cv2
from PIL import Image

from services.hand_detector import HandDetector


class DatasetCollector:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.detector = HandDetector()

    def get_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.flip(frame, 1)

        result = self.detector.detect(frame)

        frame = self.detector.draw(frame, result)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame)

        return image

    def release(self):

        self.cap.release()