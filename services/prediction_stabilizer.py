from collections import Counter


class PredictionStabilizer:

    def __init__(self, window_size=5):

        self.window_size = window_size

        self.predictions = []

        self.last_output = None

    def update(self, prediction):

        if prediction is None:
            return None

        self.predictions.append(prediction)

        if len(self.predictions) > self.window_size:
            self.predictions.pop(0)

        # Belum cukup data
        if len(self.predictions) < self.window_size:
            return None

        counter = Counter(self.predictions)

        stable_prediction = counter.most_common(1)[0][0]

        # Hindari output huruf yang sama terus-menerus
        if stable_prediction == self.last_output:
            return None

        self.last_output = stable_prediction

        self.predictions.clear()

        return stable_prediction


    def reset(self):

        self.predictions.clear()

        self.last_output = None