import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):
        if frame is None:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb)

    def draw(self, frame, result):
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame
    
    def get_landmarks(self, results):
        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    landmarks.extend([
                        lm.x,
                        lm.y,
                        lm.z
                    ])

        return landmarks