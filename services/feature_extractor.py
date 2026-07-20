import os
import csv
import cv2

from config import DATASET_PATH, PROCESSED_DATASET_PATH
from services.hand_detector import HandDetector


class FeatureExtractor:

    def __init__(self):

        self.detector = HandDetector()

        os.makedirs(PROCESSED_DATASET_PATH, exist_ok=True)


    # NORMALISASI
    # ==================================================
    def normalize_landmarks(self, landmarks):

        if len(landmarks) == 0:
            return []

        wrist_x = landmarks[0]
        wrist_y = landmarks[1]
        wrist_z = landmarks[2]

        normalized = []

        for i in range(0, len(landmarks), 3):

            normalized.append(landmarks[i] - wrist_x)
            normalized.append(landmarks[i + 1] - wrist_y)
            normalized.append(landmarks[i + 2] - wrist_z)

        return normalized


    # SCALING
    # ==================================================
    def scale_landmarks(self, landmarks):

        if len(landmarks) == 0:
            return []

        max_value = max(abs(v) for v in landmarks)

        if max_value == 0:
            return landmarks

        return [v / max_value for v in landmarks]

    # PADDING
    # ==================================================
    def padding_landmarks(self, landmarks):

        # 1 tangan
        if len(landmarks) == 63:

            landmarks.extend([0] * 63)

        # selain 63 atau 126 dianggap gagal
        elif len(landmarks) != 126:

            return None

        return landmarks


    # PREPROCESSING
    # ==================================================
    def preprocess(self, landmarks):

        landmarks = self.padding_landmarks(landmarks)

        if landmarks is None:

            return None

        landmarks = self.normalize_landmarks(landmarks)

        landmarks = self.scale_landmarks(landmarks)

        return landmarks


    # EKSTRAK DATASET
    # ==================================================
    def extract_dataset(self):

        output_csv = os.path.join(
            PROCESSED_DATASET_PATH,
            "dataset_clean.csv"
        )

        with open(output_csv, "w", newline="") as file:

            writer = csv.writer(file)

            for label in os.listdir(DATASET_PATH):

                folder = os.path.join(DATASET_PATH, label)

                if not os.path.isdir(folder):
                    continue

                print(f"Processing : {label}")

                for image_name in os.listdir(folder):

                    image_path = os.path.join(
                        folder,
                        image_name
                    )

                    image = cv2.imread(image_path)

                    if image is None:
                        continue

                    results = self.detector.detect(image)

                    landmarks = self.detector.get_landmarks(results)

                    landmarks = self.preprocess(landmarks)

                    if landmarks is None:
                        continue

                    landmarks.append(label)

                    writer.writerow(landmarks)

        print("Dataset berhasil dibuat.")

        return output_csv