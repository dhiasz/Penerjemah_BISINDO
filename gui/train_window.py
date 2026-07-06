import os
import threading
import customtkinter as ctk
from tkinter import messagebox

from config import DATASET_PATH

from services.feature_extractor import FeatureExtractor
from services.model_trainer import ModelTrainer


class TrainWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.title("Latih Model")
        self.geometry("500x650")
        

        self.extractor = FeatureExtractor()
        self.trainer = ModelTrainer()

        self.setup_ui()

        self.load_dataset_information()

        # Training otomatis saat window dibuka
        self.after(
            500,
            lambda: print("after dipanggil") or self.start_training()
        )

    

    # ==========================================================
    # GUI
    # ==========================================================

    def setup_ui(self):

        # ================= HEADER =================
        header = ctk.CTkFrame(
            self,
            height=55,
            fg_color="#D9D9D9",
            corner_radius=0
        )
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="MELATIH MODEL",
            font=("Arial", 30, "bold"),
            text_color="black"
        ).pack(pady=8)

        # ================= BODY =================
        body = ctk.CTkFrame(
            self,
            fg_color="#233E67",
            corner_radius=0
        )
        body.pack(fill="both", expand=True)

        # # Dataset
        # self.dataset_label = ctk.CTkLabel(
        #     body,
        #     text="dataset : data/dataset",
        #     font=("Arial", 18),
        #     text_color="white"
        # )
        # self.dataset_label.pack(pady=(35, 10))

        # Jumlah data
        self.total_label = ctk.CTkLabel(
            body,
            text="jumlah data : 0",
            font=("Arial", 18),
            text_color="white"
        )
        self.total_label.pack(pady=(35,10))

        # Judul Akurasi
        ctk.CTkLabel(
            body,
            text="AKURASI",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack()

        # Nilai Akurasi
        self.accuracy_label = ctk.CTkLabel(
            body,
            text="--%",
            font=("Arial", 72, "bold"),
            text_color="white"
        )

        self.accuracy_label.pack(pady=(10, 25))

        # Status
        self.status_label = ctk.CTkLabel(
            body,
            text="Status : Menunggu Training",
            font=("Arial", 18),
            text_color="white"
        )

        self.status_label.pack()

        # Progress (disembunyikan)
        self.progress = ctk.CTkProgressBar(
            body,
            width=280
        )

        self.progress.pack(pady=15)

        self.progress.set(0)

                # Tombol Latih Ulang
        self.train_button = ctk.CTkButton(
            body,
            text="LATIH ULANG",
            width=220,
            height=45,
            font=("Arial", 20, "bold"),
            command=self.start_training
        )

        self.train_button.pack(pady=(30, 25))

    # ==========================================================
    # LOAD DATASET INFO
    # ==========================================================

    def load_dataset_information(self):
        total = 0

        if os.path.exists(DATASET_PATH):

            for folder in os.listdir(DATASET_PATH):

                folder_path = os.path.join(
                    DATASET_PATH,
                    folder
                )

                if os.path.isdir(folder_path):

                    total += len(os.listdir(folder_path))

        self.total_label.configure(
            text=f"jumlah data : {total}"
        )

    # ==========================================================
    # START TRAINING
    # ==========================================================

    def start_training(self):

        
        self.accuracy_label.configure(
            text="--%"
        )

        self.status_label.configure(
            text="Status : Memulai Training...",
            text_color="white"
        )

        self.progress.set(0)

        self.train_button.configure(
            state="disabled"
        )

        thread = threading.Thread(
            target=self.training_process,
            daemon=True
        )

        thread.start()

    # ==========================================================
    # TRAINING PROCESS
    # ==========================================================

    def training_process(self):

        try:

            self.after(
                0,
                lambda: (
                    self.status_label.configure(
                        text="Status : Membaca Dataset..."
                    ),
                    self.progress.set(0.1)
                )
            )

            csv_path = self.extractor.extract_dataset()

            self.after(
                0,
                lambda: (
                    self.status_label.configure(
                        text="Status : Ekstraksi Landmark..."
                    ),
                    self.progress.set(0.3)
                )
            )

            self.after(
                0,
                lambda: (
                    self.status_label.configure(
                        text="Status : Melatih Model..."
                    ),
                    self.progress.set(0.6)
                )
            )

            result = self.trainer.train(csv_path)

            self.after(
                0,
                lambda: (
                    self.status_label.configure(
                        text="Status : Menyimpan Model..."
                    ),
                    self.progress.set(0.9)
                )
            )

            self.after(
                0,
                lambda: (
                    self.status_label.configure(
                        text="Status : Training Berhasil",
                        text_color="#FFFFFF"
                    ),
                    self.accuracy_label.configure(
                        text=f'{result["accuracy"]}%'
                    ),
                    self.progress.set(1)
                )
            )

        except FileNotFoundError:

            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Status : Dataset Tidak Ditemukan",
                    text_color="red"
                )
            )

            messagebox.showerror(
                "Error",
                "Folder dataset tidak ditemukan."
            )

        except ValueError as e:

            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Status : Training Gagal",
                    text_color="red"
                )
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

        except Exception as e:

            self.after(
                0,
                lambda: self.status_label.configure(
                    text="Status : Terjadi Kesalahan",
                    text_color="red"
                )
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            self.after(
                0,
                lambda: self.train_button.configure(
                    state="normal"
                )
            )