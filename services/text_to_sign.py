import os

from config import (
    GESTURE_WORD_PATH,
    GESTURE_ALPHABET_PATH
)

class TextToSign:

    def __init__(self):

        self.word_path = GESTURE_WORD_PATH
        self.alphabet_path = GESTURE_ALPHABET_PATH
        
# =================================================
    def get_word_image(self, word):

        filename = f"{word.lower()}.png"

        image_path = os.path.join(
            self.word_path,
            filename
        )

        if os.path.exists(image_path):
            return image_path

        return None


# =================================================
    def get_letter_image(self, letter):

        filename = f"{letter.upper()}.png"
        image_path = os.path.join(
            self.alphabet_path,
            filename
        )
        if os.path.exists(image_path):
            return image_path
        return None
    
# =================================================
    def translate(self, text):

        result = []
        words = text.strip().split()
        for word in words:
            image = self.get_word_image(word)
            if image:
                result.append({
                    "text": word.upper(),
                    "image": image,
                    "type": "word"
                })
            else:
                for letter in word:
                    image = self.get_letter_image(letter)
                    if image:
                        result.append({
                            "text": letter.upper(),
                            "image": image,
                            "type": "letter"
                        })
        return result
