import time
from config import GESTURE_HOLD_TIME

class GestureStabilizer:

    def __init__(self, hold_time=GESTURE_HOLD_TIME):

        self.hold_time = hold_time

        self.current_prediction = None
        self.start_time = None
        self.output_prediction = None

    def process(self, prediction):

        # Tidak ada gesture
        if prediction is None:
            self.current_prediction = None
            self.start_time = None
            self.output_prediction = None
            return None

        # Gesture berubah
        if prediction != self.current_prediction:
            self.current_prediction = prediction
            self.start_time = time.time()
            return None

        # Gesture sama, cek waktu
        elapsed = time.time() - self.start_time

        if elapsed >= self.hold_time:

            # Supaya tidak keluar berkali-kali
            if prediction != self.output_prediction:
                self.output_prediction = prediction
                return prediction

        return None
    
    