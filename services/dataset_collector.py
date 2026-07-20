import os
import cv2
import time

from PIL import Image
from config import DATASET_PATH
from services.camera_manager import CameraManager
from services.hand_detector import HandDetector

class DatasetCollector:

    def __init__(self):
        # Kamera
        self.camera = CameraManager()
        if not self.camera.open():
            raise RuntimeError(
                "Kamera tidak dapat dibuka."
            )
        # MediaPipe
        self.detector = HandDetector()
        # Status Capture
        self.is_capturing = False

    # PREVIEW KAMERA

    def get_frame(self):
        frame = self.camera.get_frame()
        if frame is None:
            return None

        result = self.detector.detect(frame)
        frame = self.detector.draw(
            frame,
            result
        )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        return Image.fromarray(frame)

    # BUAT FOLDER DATASET

    def create_folder(self, label):

        label = label.strip().upper()

        folder = os.path.join(
            DATASET_PATH,
            label
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        return folder

    # NOMOR FILE BERIKUTNYA

    def get_next_index(
        self,
        folder,
        label
    ):

        label = label.upper()
        numbers = []
        for filename in os.listdir(folder):
            if not filename.lower().endswith(".jpg"):
                continue
            try:
                number = int(
                    filename.replace(
                        f"{label}_",
                        ""
                    ).replace(
                        ".jpg",
                        ""
                    )
                )
                numbers.append(number)
            except ValueError:
                continue
        if len(numbers) == 0:
            return 1
        return max(numbers) + 1

    # SIMPAN GAMBAR
    def save_image(
        self,
        frame,
        folder,
        label,
        index
    ):

        filename = f"{label.upper()}_{index:03}.jpg"
        filepath = os.path.join(
            folder,
            filename
        )

        success = cv2.imwrite(
            filepath,
            frame
        )

        return success
    
# ============= BAGIAN 2 =============

    # CAPTURE DATASET
    def capture_dataset(
        self,
        label,
        total_image,
        countdown
    ):

        self.is_capturing = True
        success = 0
        failed = 0
        folder = self.create_folder(label)
        start_index = self.get_next_index(
            folder,
            label
        )

        while success < total_image and self.is_capturing:
            # COUNTDOWN

            for _ in range(countdown):
                if not self.is_capturing:
                    break
                time.sleep(1)
            if not self.is_capturing:
                break

            # AMBIL FRAME YANG BARU
            frame = self.camera.get_frame()
            if frame is None:
                failed += 1
                continue

            # DETEKSI TANGAN
            result = self.detector.detect(frame)
            if result is None or not result.multi_hand_landmarks:
                failed += 1
                continue

            # SIMPAN GAMBAR

            saved = self.save_image(
                frame,
                folder,
                label,
                start_index + success
            )

            if saved:
                success += 1
            else:
                failed += 1

        self.is_capturing = False
        return {
            "success": success,
            "failed": failed,
            "total": total_image,
            "status": "Capture selesai"
        }
    
    def stop_capture(self):
        self.is_capturing = False
    
    