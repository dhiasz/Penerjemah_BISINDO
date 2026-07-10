import cv2
from PIL import Image

from services.hand_detector import HandDetector
from services.camera_manager import CameraManager


class DatasetCollector:

    def __init__(self):

        self.camera = CameraManager()

        self.camera.open()

        self.detector = HandDetector()

    def get_frame(self):

        frame = self.camera.get_frame()

        if frame is None:
            return None

        result = self.detector.detect(frame)

        frame = self.detector.draw(frame, result)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame)

        return image

    def release(self):

        self.camera.release()