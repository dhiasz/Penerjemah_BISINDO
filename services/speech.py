import os
import uuid

from gtts import gTTS
from playsound import playsound
from config import OUTPUT_AUDIO_PATH

class Speech:

    def __init__(self):

        os.makedirs(
            OUTPUT_AUDIO_PATH,
            exist_ok=True
        )

    # =====================================
    # SPEAK
    # =====================================
    def speak(self, text):

        if not text:
            return

        filename = f"{uuid.uuid4()}.mp3"

        audio_path = os.path.join(
            OUTPUT_AUDIO_PATH,
            filename
        )

        try:
            tts = gTTS(
                text=text,
                lang="id"
            )
            tts.save(audio_path)
            playsound(audio_path)

        finally:

            if os.path.exists(audio_path):
                os.remove(audio_path)