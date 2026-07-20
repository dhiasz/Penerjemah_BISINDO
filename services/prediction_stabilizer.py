class PredictionStabilizer:

    def __init__(self, required_frames=3):

        self.required_frames = required_frames

        self.current_prediction = None
        self.prediction_count = 0

        self.accepted_prediction = None

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, prediction):

        # Tidak ada gesture
        if prediction is None:

            self.current_prediction = None
            self.prediction_count = 0
            self.accepted_prediction = None

            return None

        # Gesture berubah
        if prediction != self.current_prediction:

            self.current_prediction = prediction
            self.prediction_count = 1

            return None

        # Gesture sama
        self.prediction_count += 1

        # Belum stabil
        if self.prediction_count < self.required_frames:
            return None

        # Sudah pernah diterima
        if prediction == self.accepted_prediction:
            return None

        # Gesture stabil
        self.accepted_prediction = prediction

        return prediction

    # ==========================================
    # RESET
    # ==========================================

    def reset(self):

        self.current_prediction = None
        self.prediction_count = 0
        self.accepted_prediction = None