import customtkinter as ctk
import cv2

from PIL import Image, ImageTk
from tkinter import messagebox

from services.predictor import Predictor
from services.prediction_stabilizer import PredictionStabilizer
from services.sentence_builder import SentenceBuilder


class TranslateWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.title("Terjemahan")
        self.geometry("1000x650")
        self.resizable(False, False)

        try:

            self.predictor = Predictor()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.destroy()

            return

        self.stabilizer = PredictionStabilizer()

        self.builder = SentenceBuilder()

        self.setup_ui()

        self.update_camera()

    # ==================================================
    # GUI
    # ==================================================

    def setup_ui(self):

        # HEADER

        header = ctk.CTkFrame(
            self,
            height=55,
            fg_color="#D9D9D9",
            corner_radius=0
        )

        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="TERJEMAHAN",
            font=("Arial", 30, "bold"),
            text_color="black"
        ).pack(pady=8)

        # BODY

        body = ctk.CTkFrame(
            self,
            fg_color="#233E67",
            corner_radius=0
        )

        body.pack(fill="both", expand=True)

        # CAMERA

        self.camera_label = ctk.CTkLabel(
            body,
            text=""
        )

        self.camera_label.pack(pady=20)

        # Huruf Saat Ini

        ctk.CTkLabel(
            body,
            text="Huruf Saat Ini",
            font=("Arial",18,"bold"),
            text_color="white"
        ).pack()

        self.letter_label = ctk.CTkLabel(
            body,
            text="-",
            font=("Arial",42,"bold"),
            text_color="white"
        )

        self.letter_label.pack()

        # Hasil Sementara

        ctk.CTkLabel(
            body,
            text="Hasil Sementara",
            font=("Arial",18,"bold"),
            text_color="white"
        ).pack(pady=(15,0))

        self.word_label = ctk.CTkLabel(
            body,
            text="-",
            font=("Arial",24),
            text_color="white"
        )

        self.word_label.pack()

        # Hasil Kalimat

        ctk.CTkLabel(
            body,
            text="Hasil Kalimat",
            font=("Arial",18,"bold"),
            text_color="white"
        ).pack(pady=(15,0))

        self.sentence_label = ctk.CTkLabel(
            body,
            text="-",
            font=("Arial",24),
            text_color="white"
        )

        self.sentence_label.pack()

    # ==================================================
    # UPDATE CAMERA
    # ==================================================

    def update_camera(self):

        frame, prediction, confidence = self.predictor.predict()

        if frame is not None:

            stable_prediction = self.stabilizer.update(prediction)

            if stable_prediction is not None:

                self.builder.add_letter(stable_prediction)

                self.builder.validate_word()

            self.letter_label.configure(

                text=prediction if prediction else "-"

            )

            self.word_label.configure(

                text=self.builder.get_current_word()

            )

            sentence = self.builder.get_current_sentence()

            self.sentence_label.configure(

                text=sentence if sentence else "-"

            )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(frame)

            image = image.resize(
                (720, 320)
            )

            photo = ImageTk.PhotoImage(image)

            self.camera_label.configure(
                image=photo
            )

            self.camera_label.image = photo

        self.after(
            15,
            self.update_camera
        )

    # ==================================================
    # CLOSE
    # ==================================================

    def destroy(self):

        if hasattr(self, "predictor"):

            self.predictor.release()

        super().destroy()