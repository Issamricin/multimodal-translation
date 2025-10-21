import warnings

from argostranslate import translate

warnings.filterwarnings("ignore", category=FutureWarning,
                    module="stanza.models.tokenize.trainer")


def translate_text(text:str, lang:str, targets:list) -> list:
    """
    Translates the text provided into the desired languages (targets).

    Args:
        - text (str): The text you want to translate.
        - lang (str): The original language of the text.
        - targets (list): List of languages you want to translate to.

    Returns:
        list: List of translated texts with their target languages.
    """
    responses:list = []

    for target in targets:

        try:
            translation = translate.translate(text, lang, target)
        except AttributeError:
            responses.append({"Error": \
            f"Either of the languages may not be available, {lang, target}. Install the argos text-to-text translating language."})

            continue

        responses.append({"text": translation, "lang": target})

    return responses
