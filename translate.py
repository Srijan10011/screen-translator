<<<<<<< HEAD
from googletrans import Translator

translator = Translator()

def translate_text(text: str, dest_lang: str = "en") -> str:
    if not text.strip():
        return ""
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return ""
=======
from googletrans import Translator

translator = Translator()

def translate_text(text: str, dest_lang: str = "en") -> str:
    if not text.strip():
        return ""
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return ""
>>>>>>> 72a7d90e894f4e05a0658bdc7cfb1dce0f90ccb7
