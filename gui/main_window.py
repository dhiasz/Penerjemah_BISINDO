import customtkinter as ctk

from gui.dataset_window import DatasetWindow
from gui.train_window import TrainWindow
from gui.translate_window import TranslateWindow
from gui.input_isyara_windowt import InputIsyaratWindow
class MainWindow:

    def __init__(self):

        
        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Root
        self.root = ctk.CTk()
        self.root.title("Penerjemah Bahasa Isyarat BISINDO")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)

        self.active_window = None

        self.setup_ui()

    def setup_ui(self):

        # =================================================
        # HEADER
        # =================================================
        self.header_frame = ctk.CTkFrame(
            self.root,
            height=60,
            corner_radius=0,
            fg_color="#D9D9D9"
        )

        self.header_frame.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="PENERJEMAH BAHASA ISYARAT BISINDO",
            font=("Arial", 28, "bold"),
            text_color="black"
        )

        self.title_label.pack(pady=10)

        # =================================================
        # BODY
        # =================================================
        self.body_frame = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.body_frame.pack(fill="both", expand=True)

        # Grid Layout
        self.body_frame.grid_rowconfigure(0, weight=1)
        self.body_frame.grid_columnconfigure(1, weight=1)
        # =================================================
        # SIDEBAR
        # =================================================
        self.sidebar_frame = ctk.CTkFrame(
            self.body_frame,
            width=300,
            corner_radius=0,
            fg_color="#17345D"
        )

        self.sidebar_frame.grid(
            row=0,
            column=0,
            sticky="ns"
        )



        # Dashboard
        self.dashboard_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            text_color="white"
        )

        self.dashboard_label.pack(pady=15)


        # Tombol Dataset
        self.btn_dataset = ctk.CTkButton(
            self.sidebar_frame,
            text="Tambah Dataset",
            width=200,
            height=55,
            font=("Arial", 18, "bold"),
            command=self.open_dataset
        )

        self.btn_dataset.pack(pady=15)

        # Tombol Train
        self.btn_train = ctk.CTkButton(
            self.sidebar_frame,
            text="Latih Model",
            width=200,
            height=55,
            font=("Arial", 18, "bold"),
            command=self.open_train
        )

        self.btn_train.pack(pady=15)

        # Tombol Translate
        self.btn_translate = ctk.CTkButton(
            self.sidebar_frame,
            text="Terjemahan",
            width=200,
            height=55,
            font=("Arial", 18, "bold"),
            command=self.open_translate
        )

        self.btn_translate.pack(pady=15)

        # Tombol Bahasa Isyarat
        self.btn_sign = ctk.CTkButton(
            self.sidebar_frame,
            text="Bahasa Isyarat",
            width=200,
            height=55,
            font=("Arial", 18, "bold"),
            command=self.open_text_to_sign
        )

        self.btn_sign.pack(pady=15)

        # memperpanjang
        # ==================================
        self.btn_dataset = ctk.CTkButton(
            self.sidebar_frame,
            text="",
            width=300,
            height=55,
            font=("Arial", 18, "bold"),
            fg_color="#17345D"
        )

        self.btn_dataset.pack(pady=15)
        # ================================== 

        # WAJIB AGAR WIDTH BERFUNGSI
        self.sidebar_frame.grid_propagate(False)

        # =================================================
        # CONTENT FRAME
        # =================================================
        self.content_frame = ctk.CTkFrame(
            self.body_frame,
            corner_radius=0,
            fg_color="#F3F3F3"
        )

        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # Judul
        self.welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Selamat Datang",
            font=("Arial", 32, "bold"),
            text_color="#1F2937"
        )

        self.welcome_label.pack(pady=(60, 30))

        # Deskripsi
        description = (
            "Aplikasi penerjemah bahasa isyarat BISINDO berbasis\n"
            "Computer Vision dan Machine Learning.\n\n"
            "Antarmuka ini dirancang untuk menyediakan:\n\n"
            "• Penambahan dataset\n"
            "• Pelatihan model\n"
            "• Penerjemahan bahasa isyarat menjadi teks dan suara\n"
            "• Penampilan bahasa isyarat berdasarkan masukan pengguna\n\n"
            "Sehingga pengguna dapat berinteraksi dengan\n"
            "sistem secara lebih mudah dan terstruktur."
        )

        self.description_label = ctk.CTkLabel(
            self.content_frame,
            text=description,
            font=("Arial", 20),
            justify="left",
            text_color="#374151"
        )

        self.description_label.pack(padx=50)

    def open_window(self, window_class):

            if self.active_window is not None and self.active_window.winfo_exists():
                self.active_window.focus_force()
                return

            self.active_window = window_class(self.root)

            def on_close():
                self.active_window.destroy()
                self.active_window = None

            self.active_window.protocol(
                "WM_DELETE_WINDOW",
                on_close
            )

    # =================================================
    # EVENT BUTTON
    # =================================================
    def open_dataset(self):
        self.open_window(DatasetWindow)

    def open_train(self):
        self.open_window(TrainWindow)

    def open_translate(self):
        self.open_window(TranslateWindow)

    def open_text_to_sign(self):
        self.open_window(InputIsyaratWindow)

    # =================================================
    # RUN
    # =================================================
    def run(self):
        self.root.mainloop()