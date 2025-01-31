from .english import ENGLISH

class GetLanguage:
    def get_language(self, language):
        if language == "en":
            return ENGLISH
        else:
            raise NotImplementedError(f"Language {language} is not supported.")