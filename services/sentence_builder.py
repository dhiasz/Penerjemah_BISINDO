import pandas as pd

from config import DICTIONARY_PATH


class SentenceBuilder:

    def __init__(self):

        self.dictionary = self.load_dictionary()

        self.current_word = ""

        self.current_sentence = ""

    # meload kbbi
    def load_dictionary(self):

        data = pd.read_csv(DICTIONARY_PATH)

        words = set()

        for word in data["kata"]:

            if pd.isna(word):
                continue

            word = str(word).strip().upper()

            if word:

                words.add(word)

        print(f"Kamus dimuat : {len(words)} kata")

        return words

    
    # menambah kata

    def add_letter(self, letter):

        if letter is None:
            return

        self.current_word += letter.upper()


    def validate_word(self):

        word = self.current_word.strip()

        if word in self.dictionary:

            if self.current_sentence == "":

                self.current_sentence = word

            else:

                self.current_sentence += " " + word

            self.current_word = ""

            return True

        return False


    def backspace(self):

        self.current_word = self.current_word[:-1]


    def reset(self):

        self.current_word = ""

        self.current_sentence = ""


    def get_current_word(self):

        return self.current_word

    def get_current_sentence(self):

        return self.current_sentence