from googletrans import Translator


class TranslationFacade():
    def __init__(self):
        self._langs = {
            "ja": "Japanese",
            "he": "Hebrew",
            "en": "English",
            "es": "Spanish",
        }

    def translate(self, text, target_lang):
        translator = Translator()
        result = translator.translate(text, target_lang)
        return result.text

    def language_in_english(self, lang):
        return self._langs[lang]
