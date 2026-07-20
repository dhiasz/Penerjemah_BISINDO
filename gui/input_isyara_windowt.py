import customtkinter as ctk
import re

from PIL import Image, ImageTk

from services.text_to_sign import TextToSign

class InputIsyaratWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        # =====================================
        # SERVICE
        # =====================================
        self.text_to_sign = TextToSign()

        # =====================================
        # VARIABLE
        # =====================================
        self.gesture_list = []
        self.current_index = 0
        self.after_id = None

        # =====================================
        # SETUP
        # =====================================
        self.setup_window()
        self.setup_ui()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # =====================================
    # WINDOW
    # =====================================
    def setup_window(self):

        self.title("Menampilkan Bahasa Isyarat")

        self.geometry("500x520")

        self.resizable(False, False)

        self.grab_set()

    # =====================================
    # UI
    # =====================================
    def setup_ui(self):

        # -----------------------------
        # Judul
        # -----------------------------
        self.title_label = ctk.CTkLabel(
            self,
            text="MENAMPILKAN BAHASA ISYARAT",
            font=("Arial", 22, "bold")
        )

        self.title_label.pack(
            pady=(15, 20)
        )
        

        # -----------------------------
        # Form
        # -----------------------------
        self.form_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.form_frame.pack(
            fill="x",
            padx=20
        )

        self.input_label = ctk.CTkLabel(
            self.form_frame,
            text="Input Text :",
            font=("Arial", 15)
        )

        self.input_label.pack(
            anchor="w"
        )

        self.input_entry = ctk.CTkEntry(
            self.form_frame,
            height=35
        )

        self.input_entry = ctk.CTkEntry(
            self.form_frame,
            height=35
        )

        self.input_entry.pack(
            fill="x"
        )

        self.input_info = ctk.CTkLabel(
            self.form_frame,
            text="Tidak dapat memasukkan karakter khusus seperti @ # $ % &",
            font=("Arial", 12),
            text_color="red"
        )

        self.input_info.pack(
            anchor="w",
            pady=(3, 10)
        )

        self.input_entry.pack(
            fill="x",
            pady=(5, 10)
        )

        self.input_info = ctk.CTkLabel(
            self.form_frame,
            text="Hanya huruf dan spasi yang diperbolehkan.",
            text_color="red"
        )
        self.input_info.pack(anchor="w", pady=(3, 10))
        # Awalnya disembunyikan
        self.input_info.pack_forget()

        # -----------------------------
        # Button
        # -----------------------------
        self.show_button = ctk.CTkButton(
            self.form_frame,
            text="Tampilkan",
            width=140,
            height=40,
            command=self.show_gesture
        )

        self.show_button.pack(
            anchor="w"
        )

        # -----------------------------
        # Output
        # -----------------------------
        self.output_frame = ctk.CTkFrame(
            self,
            width=450,
            height=260,
            fg_color="#F0A000",
            corner_radius=0
        )

        self.output_frame.pack(
            padx=20,
            pady=20
        )

        self.output_frame.pack_propagate(False)

        self.image_label = ctk.CTkLabel(
            self.output_frame,
            text="Output Gambar",
            font=("Arial", 18),
            text_color="white"
        )

        self.image_label.pack(
            expand=True
        )

    # =====================================
    # EVENT
    # =====================================
    def show_gesture(self):

        text = self.input_entry.get().strip()
        
        if text == "":
            return

        if not self.validate_input(text):
            self.input_info.configure(
                text="Hanya huruf dan spasi yang diperbolehkan."
            )
            return

        self.input_info.configure(text="")

        if self.after_id is not None:
            self.after_cancel(
                self.after_id
            )
            self.after_id = None

        self.gesture_list = self.text_to_sign.translate(text)
        if not self.gesture_list:
            return
        
        self.current_index = 0
        self.show_current_gesture()
    
    def show_next_gesture(self):

        self.current_index += 1
        self.show_current_gesture()

    # Validasi
    def validate_input(self, text):

        pattern = r"^[A-Za-z\s]+$"
        return re.fullmatch(pattern, text) is not None

    # =====================================
    # MENAMPILKAN SATU GAMBAR
    # =====================================
    def show_current_gesture(self):

        if len(self.gesture_list) == 0:
            return
        gesture = self.gesture_list[self.current_index]
        with Image.open(gesture["image"]) as image:

            image = image.resize((300, 220))
            photo = ImageTk.PhotoImage(image)

        self.image_label.configure(
            image=photo,
            text=""
        )

        self.image_label.image = photo
        # Jika masih ada gambar berikutnya
        if self.current_index < len(self.gesture_list) - 1:

            self.after_id = self.after(
                1000,
                self.show_next_gesture
            )

    # =====================================
    # CLOSE
    # =====================================
    def on_close(self):

        if self.after_id is not None:
            self.after_cancel(
                self.after_id
            )
        self.destroy()
