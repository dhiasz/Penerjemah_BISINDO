import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

from config import MODEL_PATH


class ModelTrainer:

    def __init__(self):

        self.model = GradientBoostingClassifier(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )

    # ==========================================
    # LOAD DATASET
    # ==========================================
    def load_dataset(self, csv_path):

        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"Dataset tidak ditemukan : {csv_path}"
            )

        data = pd.read_csv(
            csv_path,
            header=None
        )

        if data.empty:
            raise ValueError(
                "Dataset kosong."
            )

        return data

    # ==========================================
    # SPLIT DATA
    # ==========================================
    def split_dataset(self, data):

        X = data.iloc[:, :-1]

        y = data.iloc[:, -1]

        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

    # ==========================================
    # TRAIN MODEL
    # ==========================================
    def train_model(self, X_train, y_train):

        self.model.fit(
            X_train,
            y_train
        )

    # ==========================================
    # EVALUASI
    # ==========================================
    def evaluate_model(self, X_test, y_test):

        prediction = self.model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            prediction
        )

        return accuracy

    # ==========================================
    # SIMPAN MODEL
    # ==========================================
    def save_model(self):

        os.makedirs(
            os.path.dirname(MODEL_PATH),
            exist_ok=True
        )

        joblib.dump(
            self.model,
            MODEL_PATH
        )

    # ==========================================
    # TRAINING
    # ==========================================
    def train(self, csv_path):

        data = self.load_dataset(csv_path)

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = self.split_dataset(data)

        self.train_model(
            X_train,
            y_train
        )

        accuracy = self.evaluate_model(
            X_test,
            y_test
        )

        self.save_model()

        return {

            "dataset_path": csv_path,

            "jumlah_data": len(data),

            "accuracy": round(
                accuracy * 100,
                2
            ),

            "status": "Selesai"

        }