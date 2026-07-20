class Translator:

    def __init__(self):

        self.current_word = ""

    # =====================================
    # TAMBAH HURUF
    # =====================================

    def add_letter(self, letter):

        if letter is None:
            return self.current_word

        self.current_word += letter

        return self.current_word

    # =====================================
    # HAPUS HURUF TERAKHIR
    # =====================================

    def remove_letter(self):

        if self.current_word:

            self.current_word = self.current_word[:-1]

        return self.current_word

    # =====================================
    # AMBIL KATA SAAT INI
    # =====================================

    def get_current_word(self):

        return self.current_word

    # =====================================
    # RESET KATA
    # =====================================

    def clear(self):

        self.current_word = ""
        return self.current_word
    
    # =====================================
    # SELESAIKAN KATA
    # =====================================

    def finish_word(self):
        word = self.current_word
        self.current_word = ""
        return word