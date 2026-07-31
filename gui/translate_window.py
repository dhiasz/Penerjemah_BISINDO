import customtkinter as ctk
import cv2

from PIL import Image, ImageTk
from services.camera_manager import CameraManager
from tkinter import messagebox

from services.predictor import Predictor
from services.translator import Translator
from services.kbbi_corrector import KBBICorrector
from services.sentence_builder import SentenceBuilder
from services.speech import Speech

# from services.prediction_stabilizer import PredictionStabilizer
from services.gesture_stabilizer import GestureStabilizer


class TranslateWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)
        # ======== CAMERA ==========
        self.camera = CameraManager()

        # ======== PREDICTOR ==========
        self.predictor = Predictor()

        # ======== TRANSLATOR ==========
        self.translator = Translator()

        # # ======== HASIL KALIMAT ========
        self.sentence_builder = SentenceBuilder()

        # ======= KBBI CORRECTOR ========
        self.corrector = KBBICorrector()

        # ======== SPEECH ========
        self.speech = Speech()

        # ======== PREDICT STABILIZER ========
        # self.stabilizer = PredictionStabilizer(required_frames=3)

        # ======== GESTURE STABILIZER ========
        self.stabilizer = GestureStabilizer()

        self.setup_window()
        self.setup_ui()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )
        
        self.after_id = None

    # =====================================
    # WINDOW
    # =====================================

    def setup_window(self):

        self.title("Terjemahan Bahasa Isyarat")
        self.geometry("1280x720")
        # self.resizable(False, False)
        self.grab_set()

    # =====================================
    # UI
    # =====================================

    def setup_ui(self):

        # =====================================
        # JUDUL
        # =====================================
        self.title_label = ctk.CTkLabel(
            self,
            text="TERJEMAHAN BAHASA ISYARAT",
            font=("Arial", 22, "bold")
        )

        self.title_label.pack(
            pady=(15, 20)
        )

        # =====================================
        # CONTAINER
        # =====================================
        self.top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.top_frame.pack(
            fill="x",
            padx=20,
            pady=(0,20)
        )

        # 3 kolom
        self.top_frame.grid_columnconfigure(0, weight=1)   
        self.top_frame.grid_columnconfigure(1, weight=0)   
        self.top_frame.grid_columnconfigure(2, weight=1)   

        # ==================================================
        # BISINDO
        # ==================================================
        self.bisindo_frame = ctk.CTkFrame(
            self.top_frame,
            width=260,
            height=260,
            fg_color="transparent"
        )

        self.bisindo_frame.grid(
            row=0,
            column=0,
            sticky="e",
            padx=(0,30)
        )

        self.bisindo_frame.grid_propagate(False)

        bisindo_image = Image.open("assets/images/bisindo.png")
        bisindo_image = bisindo_image.resize((260,260))

        self.bisindo_photo = ImageTk.PhotoImage(bisindo_image)

        self.bisindo_label = ctk.CTkLabel(
            self.bisindo_frame,
            image=self.bisindo_photo,
            text=""
        )

        self.bisindo_label.pack(expand=True)

        # ==================================================
        # CAMERA
        # ==================================================
        self.camera_frame = ctk.CTkFrame(
            self.top_frame,
            width=500,
            height=260,
            fg_color="#F0A000",
            corner_radius=0
        )

        self.camera_frame.grid(
            row=0,
            column=1
        )

        self.camera_frame.grid_propagate(False)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="Preview Kamera",
            font=("Arial",18),
            text_color="white"
        )

        self.camera_label.pack(expand=True)

        # ==================================================
        # SPACER KANAN
        # ==================================================
        self.right_space = ctk.CTkFrame(
            self.top_frame,
            width=250,
            height=260,
            fg_color="transparent"
        )

        self.right_space.grid(
            row=0,
            column=2,
            sticky="w"
        )

        self.right_space.grid_propagate(False)

        # Bagian huruf saat ini
        # =========================================
        self.current_letter_label = ctk.CTkLabel(
            self,
            text="Huruf Saat Ini :",
            font=("Arial",15)
        )

        self.current_letter_label.pack(
            anchor="w",
            padx=20
        )

        self.current_letter_entry = ctk.CTkEntry(
            self,
            height=35
        )

        self.current_letter_entry.pack(
            fill="x",
            padx=20,
            pady=(5,15)
        )

        self.current_letter_entry.configure(
            state="readonly"
        )
        # =========================================

        # Hasil Sementara
        # =========================================
        self.temp_result_label = ctk.CTkLabel(
            self,
            text="Hasil Sementara :",
            font=("Arial",15)
        )

        self.temp_result_label.pack(
            anchor="w",
            padx=20
        )

        self.temp_result_entry = ctk.CTkEntry(
            self,
            height=35
        )

        self.temp_result_entry.pack(
            fill="x",
            padx=20,
            pady=(5,15)
        )

        self.temp_result_entry.configure(
            state="readonly"
        )
        # =========================================

        # Hasil Kalimat
        # =========================================
        self.sentence_label = ctk.CTkLabel(
            self,
            text="Hasil Kalimat :",
            font=("Arial",15)
        )

        self.sentence_label.pack(
            anchor="w",
            padx=20
        )

        self.sentence_textbox = ctk.CTkTextbox(
            self,
            height=80
        )

        self.sentence_textbox.pack(
            fill="x",
            padx=20,
            pady=(5,15)
        )

        self.sentence_textbox.configure(
            state="disabled"
        )
        # =========================================

        # Setatus system
        self.status_label = ctk.CTkLabel(
            self,
            text="Status Sistem :",
            font=("Arial",15)
        )

        self.status_label.pack(
            anchor="w",
            padx=20
        )

        self.status_value = ctk.CTkLabel(
            self,
            text="Menunggu Gesture...",
            font=("Arial",13),
            text_color="green"
        )

        self.status_value.pack(
            anchor="w",
            padx=20,
            pady=(5,15)
        )

        # =====================================
        # START CAMERA
        # =====================================

        if self.camera.open():
            self.update_camera()
        else:
            messagebox.showerror(
                "Error",
                "Kamera tidak dapat dibuka."
            )

    # =====================================
    # UPDATE CAMERA
    # =====================================

    def update_camera(self):

        frame = self.camera.get_frame()
        if frame is None:
            self.after_id = self.after(
                10,
                self.update_camera
            )
            return

        display_frame, prediction, confidence = self.predictor.predict(frame)
        prediction = self.stabilizer.process(prediction)
        if prediction is None:
            self.set_current_letter("")
        else:
            self.set_current_letter(prediction)
            if not self.process_special_gesture(prediction):
                self.process_prediction(prediction)

        # Frame untuk ditampilkan di GUI
        
        display_frame = cv2.cvtColor(
            display_frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(display_frame)
        image = image.resize((500, 260))
        photo = ImageTk.PhotoImage(image)

        self.camera_label.configure(
            image=photo,
            text=""
        )

        self.camera_label.image = photo
        self.after_id = self.after(
            10,
            self.update_camera
        )

    # =====================================
    # Current Letter (kata saat ini)
    # =====================================
    def set_current_letter(self, letter):

        self.current_letter_entry.configure(
            state="normal"
        )

        self.current_letter_entry.delete(
            0,
            "end"
        )

        self.current_letter_entry.insert(
            0,
            letter
        )

        self.current_letter_entry.configure(
            state="readonly"
        )

    # =====================================
    # SET HASIL SEMENTARA
    # =====================================

    def set_temp_result(self, text):
        
        self.temp_result_entry.configure(
            state="normal"
        )

        self.temp_result_entry.delete(
            0,
            "end"
        )

        self.temp_result_entry.insert(
            0,
            text
        )

        self.temp_result_entry.configure(
            state="readonly"
        )

    # =====================================
    # PROCESS PREDICTION
    # =====================================
    def process_prediction(self, prediction):

        if prediction is None:
            return

        current_word = self.translator.add_letter(prediction)

        self.set_temp_result(current_word)

    # =====================================
    # SET HASIL KALIMAT
    # =====================================

    def set_sentence(self, text):
        self.sentence_textbox.configure(
            state="normal"
        )

        self.sentence_textbox.delete(
            "1.0",
            "end"
        )

        self.sentence_textbox.insert(
            "end",
            text
        )

        self.sentence_textbox.configure(
            state="disabled"
        )

    # =====================================
    # SPECIAL GESTURE
    # =====================================

    def process_special_gesture(self, prediction):
        if prediction == "BACKSPACE":
            # Hapus huruf terakhir
            current_word = self.translator.remove_letter()

            # Update GUI
            self.set_temp_result(current_word)
            self.set_current_letter("")

            return True

        if prediction == "SPACE":
            # Reset state huruf
            
            # Selesaikan kata
            word = self.translator.finish_word()

            if not word:
                self.set_temp_result("")
                self.set_current_letter("")
                return True

            word = self.corrector.correct(word)
            sentence = self.sentence_builder.add_word(word)
            self.set_sentence(sentence)
            self.speech.speak(word)
            self.set_temp_result("")
            self.set_current_letter("")

            return True

        return False
    
    # =====================================
    # SET STATUS
    # =====================================

    def set_status(self, text, color="green"):

        self.status_value.configure(
            text=text,
            text_color=color
        )

    # =====================================
    # CLOSE
    # =====================================
    def on_close(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)

        self.camera.release()
        self.destroy()