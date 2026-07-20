import cv2

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS
)

class CameraManager:

    def __init__(self):

        self.camera_index = CAMERA_INDEX
        self.cap = None

    # Bagian membaca list kamera
    def get_available_cameras(self):

        cameras = []
        for index in range(10):
            cap = cv2.VideoCapture(index)

            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    cameras.append(index)

            cap.release()

        return cameras

    # Buka kamera
    def open(self, index=None):
        if index is not None:
            self.camera_index = index
        self.release()
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        self.cap.set(
            cv2.CAP_PROP_FPS,
            CAMERA_FPS
        )

        if self.cap is None:
            return False

        return self.cap.isOpened()


    def get_frame(self):
        if self.cap is None:
            return None

        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        return frame

    # Ganti kamera
    def change_camera(self, index):
        return self.open(index)


    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def is_open(self):
        return self.cap is not None and self.cap.isOpened()
    
    def __del__(self):
        self.release()

