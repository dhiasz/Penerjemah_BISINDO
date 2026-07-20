import pandas as pd

from config import DICTIONARY_PATH


class KBBICorrector:

    def __init__(self):

        self.words = self.load_dictionary()

    # =====================================
    # LOAD DICTIONARY
    # =====================================

    def load_dictionary(self):

        df = pd.read_csv(
            DICTIONARY_PATH
        )

        return set(
            word.upper()
            for word in df["kata"].dropna()
        )

    # =====================================
    # CHECK WORD
    # =====================================

    def exists(self, word):

        return word.upper() in self.words

    # =====================================
    # CORRECT WORD
    # =====================================

    def correct(self, word):

        if self.exists(word):

            return word

        return word