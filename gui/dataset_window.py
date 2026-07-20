import threading
import customtkinter as ctk

from tkinter import messagebox
from PIL import ImageTk
from services.dataset_collector import DatasetCollector

class DatasetWindow(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        # ===============================
        # SERVICE
        # ===============================
        self.collector = DatasetCollector()

        # ===============================
        # VARIABLE
        # ===============================
        self.camera_job = None

        # ===============================
        # SETUP
        # ===============================
        self.setup_window()
        self.setup_ui()

        # Mulai preview kamera
        self.update_camera()

        # ===============================
        # EVENT
        # ===============================
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # ==================================
    # WINDOW
    # ==================================
    def setup_window(self):

        self.title("Tambah Dataset")
        self.geometry("1280x720")
        # self.resizable(False, False)
        self.grab_set()

    # ==================================
    # UI
    # ==================================
    def setup_ui(self):

        # ==================================
        # TITLE
        # ==================================
        self.title_label = ctk.CTkLabel(
            self,
            text="TAMBAH DATASET",
            font=("Arial", 22, "bold")
        )

        self.title_label.pack(pady=(15, 20))

        # ==================================
        # FORM
        # ==================================
        self.form_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.form_frame.pack(
            fill="x",
            padx=20
        )

        # -----------------------------
        # Label
        # -----------------------------
        self.label_title = ctk.CTkLabel(
            self.form_frame,
            text="Masukkan Label :",
            font=("Arial", 15)
        )

        self.label_title.grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.label_entry = ctk.CTkEntry(
            self.form_frame,
            width=220
        )

        self.label_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.label_info = ctk.CTkLabel(
            self.form_frame,
            text="* Contoh: A, B, HALO",
            font=("Arial", 12),
            text_color="red"
        )

        self.label_info.grid(
            row=0,
            column=2,
            padx=(5, 0),
            sticky="w"
        )

        # -----------------------------
        # Jumlah Gambar
        # -----------------------------
        self.total_title = ctk.CTkLabel(
            self.form_frame,
            text="Jumlah Gambar :",
            font=("Arial", 15)
        )

        self.total_title.grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.total_entry = ctk.CTkEntry(
            self.form_frame,
            width=220
        )

        self.total_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        self.total_info = ctk.CTkLabel(
            self.form_frame,
            text="* Contoh: 100",
            font=("Arial", 12),
            text_color="red"
        )

        self.total_info.grid(
            row=1,
            column=2,
            padx=(5, 0),
            sticky="w"
        )

        # -----------------------------
        # Countdown
        # -----------------------------
        self.countdown_title = ctk.CTkLabel(
            self.form_frame,
            text="Hitung Mundur :",
            font=("Arial", 15)
        )

        self.countdown_title.grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.countdown_entry = ctk.CTkEntry(
            self.form_frame,
            width=220
        )

        self.countdown_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=5
        )

        self.countdown_info = ctk.CTkLabel(
            self.form_frame,
            text="* Dalam detik (misal: 5)",
            font=("Arial", 12),
            text_color="red"
        )

        self.countdown_info.grid(
            row=2,
            column=2,
            padx=(5, 0),
            sticky="w"
        )

        # ==================================
        # CAMERA
        # ==================================
        self.camera_frame = ctk.CTkFrame(
            self,
            width=1080,
            height=400,
            fg_color="#E8E8E8",
            corner_radius=8
        )

        self.camera_frame.pack(
            padx=20,
            pady=20
        )

        self.camera_frame.pack_propagate(False)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="Camera Preview",
            font=("Arial", 18)
        )

        self.camera_label.pack(
            expand=True
        )

        # ==================================
        # BUTTON
        # ==================================
        self.capture_button = ctk.CTkButton(
            self,
            text="Simpan Gesture",
            width=180,
            height=40,
            command=self.start_capture
        )

        self.capture_button.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # ==================================
    # EVENT
    # ==================================
    def start_capture(self):

        label = self.label_entry.get().strip()

        total = self.total_entry.get().strip()

        countdown = self.countdown_entry.get().strip()

        # ==========================
        # VALIDASI
        # ==========================
        if label == "":
            messagebox.showwarning(
                "Peringatan",
                "Label belum diisi."
            )
            return

        try:
            total = int(total)
            countdown = int(countdown)

        except ValueError:

            messagebox.showwarning(
                "Peringatan",
                "Jumlah gambar dan hitung mundur harus berupa angka."
            )

            return

        # Disable tombol
        self.capture_button.configure(
            state="disabled"
        )

        # Jalankan thread
        thread = threading.Thread(

            target=self.capture_process,

            args=(
                label,
                total,
                countdown
            ),

            daemon=True
        )

        thread.start()

    def capture_process(
        self,
        label,
        total,
        countdown
    ):

        result = self.collector.capture_dataset(

            label,
            total,
            countdown

        )

        self.after(
            0,
            lambda: self.capture_finished(result)
        )

    def capture_finished(self, result):

        self.capture_button.configure(
            state="normal"
        )

        messagebox.showinfo(

            "Informasi",

            f"""
    Capture selesai

    Berhasil : {result['success']}
    Gagal    : {result['failed']}
    Total    : {result['total']}
    """
        )

    def stop_capture(self):

        self.collector.stop_capture()

    # ==================================
    # UPDATE CAMERA
    # ==================================
    def update_camera(self):

        image = self.collector.get_frame()

        if image is not None:
            photo = ImageTk.PhotoImage(image)
            self.camera_label.configure(
                image=photo,
                text=""
            )

            self.camera_label.image = photo

        self.camera_job = self.after(
            30,
            self.update_camera
        )

    # ==================================
    # CLOSE
    # ==================================
    def on_close(self):

        if self.camera_job is not None:
            self.after_cancel(self.camera_job)

        self.collector.camera.release()

        self.destroy()