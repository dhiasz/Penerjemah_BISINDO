import os
import cv2
import joblib
import numpy as np

from config import MODEL_PATH, CONFIDENCE_THRESHOLD
from services.hand_detector import HandDetector
from services.feature_extractor import FeatureExtractor


class Predictor:

    def __init__(self):

        self.detector = HandDetector()

        self.extractor = FeatureExtractor()

        self.cap = cv2.VideoCapture(0)

        self.model = self.load_model()

    # ==========================================
    # LOAD MODEL
    # ==========================================
    def load_model(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                "Model belum tersedia. Silakan lakukan training terlebih dahulu."
            )

        return joblib.load(MODEL_PATH)

    # ==========================================
    # GET FRAME
    # ==========================================
    def get_frame(self):

        success, frame = self.cap.read()

        if not success:

            return None

        frame = cv2.flip(frame, 1)

        return frame

    # ==========================================
    # PREDICT
    # ==========================================
    def predict(self):

        frame = self.get_frame()

        if frame is None:

            return None, None, 0

        results = self.detector.detect(frame)

        frame = self.detector.draw(frame, results)

        landmarks = self.detector.get_landmarks(results)

        landmarks = self.extractor.preprocess(landmarks)

        if landmarks is None:

            return frame, None, 0

        sample = np.array(landmarks).reshape(1, -1)

        prediction = self.model.predict(sample)[0]

        probabilities = self.model.predict_proba(sample)[0]

        confidence = max(probabilities)

        confidence_percent = round(confidence * 100, 2)

        if confidence < CONFIDENCE_THRESHOLD:

            return frame, None, confidence_percent

        return frame, prediction, confidence_percent

    # ==========================================
    # RELEASE CAMERA
    # ==========================================
    def release(self):

        if self.cap.isOpened():

            self.cap.release()