class SentenceBuilder:

    def __init__(self):
        self.words = []

    # =====================================
    # TAMBAH KATA
    # =====================================
    def add_word(self, word):

        if not word:
            return self.get_sentence()

        self.words.append(word)

        return self.get_sentence()

    # =====================================
    # AMBIL KALIMAT
    # =====================================
    def get_sentence(self):

        return " ".join(self.words)

    # =====================================
    # HAPUS KATA TERAKHIR
    # =====================================
    def remove_last_word(self):

        if self.words:

            self.words.pop()

        return self.get_sentence()

    # =====================================
    # RESET
    # =====================================
    def clear(self):

        self.words.clear()

        return ""