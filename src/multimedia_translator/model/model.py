from enum import Enum
from io import BytesIO

LANGUAGE = Enum(
    "LANGUAGE",
    [
        "ar",
        "az",
        "bg",
        "bn",
        "ca",
        "cs",
        "da",
        "de",
        "el",
        "en",
        "eo",
        "es",
        "et",
        "eu",
        "fa",
        "fi",
        "fr",
        "ga",
        "gl",
        "he",
        "hi",
        "hu",
        "id",
        "it",
        "ja",
        "ko",
        "ky",
        "lt",
        "lv",
        "ms",
        "nb",
        "nl",
        "pt-BR",
        "pl",
        "pt",
        "ro",
        "ru",
        "sk",
        "sl",
        "sq",
        "sr",
        "sv",
        "th",
        "tl",
        "tr",
        "uk",
        "ur",
        "vi",
        "zh-Hans",
        "zh-Hant",
    ],
)


class TextModel:

    def __init__(self, title: str, lang: LANGUAGE) -> None:
        self.__title = title
        self.__lang = lang

    @property
    def title(self) -> str:
        return self.__title

    @property
    def lang(self) -> LANGUAGE:
        """
        The text language
        """
        return self.__lang


class TextTransModel(TextModel):

    def __init__(self, title: str, lang: LANGUAGE, targets: list[LANGUAGE]) -> None:
        super().__init__(title, lang)
        self.__targets = targets

    @property
    def targets(self) -> list[LANGUAGE]:
        return self.__targets


class BodyTransModel(TextTransModel):
    """
    It contains title and body
    """

    def __init__(self, title: str, lang: LANGUAGE, targets: list[LANGUAGE], body: str) -> None:
        super().__init__(title, lang, targets)
        self.__body = body

    @property
    def body(self) -> str:
        return self.__body


# https://docs.python.org/3/library/io.html#binary-i-o
class AudioVideoImageTransModel(TextTransModel):
    def __init__(
        self, title: str, lang: LANGUAGE, targets: list[LANGUAGE], byte_stream: BytesIO
    ) -> None:
        super().__init__(title, lang, targets)
        self.__byte_stream = byte_stream


class ValidationError:
    def __init__(self, cause: str) -> None:
        self.__cause = cause

    @property
    def cause(self) -> str:
        return self.__cause


if __name__ == "__main__":
    model = TextTransModel("who cases", LANGUAGE.en, [LANGUAGE.sv, LANGUAGE.bg])
    print(model.title)
    print(model.lang.name)
    f = BytesIO(b"some initial binary data: \x00\x01")
