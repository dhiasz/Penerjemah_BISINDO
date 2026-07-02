import customtkinter as ctk

from PIL import ImageTk

from services.dataset_collector import DatasetCollector


class DatasetWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.title("Tambah Dataset")
        self.geometry("1000x650")

        self.collector = DatasetCollector()

        self.setup_ui()

        self.update_camera()

    def setup_ui(self):

        # ================= HEADER =================

        header_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#D9D9D9",
            height=50
        )

        header_frame.pack(fill="x")

        title = ctk.CTkLabel(
            header_frame,
            text="TAMBAH DATASET",
            font=("Arial", 24, "bold"),
            text_color="black"
        )

        title.pack(pady=10)

        # ================= INPUT =================

        form_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        form_frame.pack(anchor="w", padx=20, pady=20)

        ctk.CTkLabel(
            form_frame,
            text="Masukan Label :",
            font=("Arial", 18)
        ).grid(row=0, column=0, sticky="w")

        self.label_entry = ctk.CTkEntry(
            form_frame,
            width=200
        )

        self.label_entry.grid(row=0, column=1, padx=20)

        ctk.CTkLabel(
            form_frame,
            text="Jumlah Gambar :",
            font=("Arial", 18)
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.jumlah_entry = ctk.CTkEntry(
            form_frame,
            width=200
        )

        self.jumlah_entry.insert(0, "100")

        self.jumlah_entry.grid(row=1, column=1)

        ctk.CTkLabel(
            form_frame,
            text="Hitung Mundur :",
            font=("Arial", 18)
        ).grid(row=2, column=0, sticky="w")

        self.countdown_entry = ctk.CTkEntry(
            form_frame,
            width=200
        )

        self.countdown_entry.insert(0, "5")

        self.countdown_entry.grid(row=2, column=1)

        # ================= CAMERA =================

        self.camera_frame = ctk.CTkFrame(
            self,
            width=850,
            height=300
        )

        self.camera_frame.pack(pady=20)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text=""
        )

        self.camera_label.pack()

        # ================= BUTTON =================

        self.save_button = ctk.CTkButton(
            self,
            text="Simpan Gestur"
        )

        self.save_button.pack(
            anchor="w",
            padx=20
        )

    def update_camera(self):

        image = self.collector.get_frame()

        if image is not None:

            image = image.resize(
                (850, 300)
            )

            photo = ImageTk.PhotoImage(image)

            self.camera_label.configure(
                image=photo
            )

            self.camera_label.image = photo

        self.after(
            10,
            self.update_camera
        )

    def destroy(self):

        self.collector.release()

        super().destroy()