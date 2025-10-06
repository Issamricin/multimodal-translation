from argostranslate import translate

import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")


def translate_text(text:str, lang:str, targets:list) -> list:
    """
    Turns the translating library server on each time it is called.
    After translating it stops the server.
    Translates the text provided into the desired languages (targets).

    Args:
        - text (str): The text you want to translate.
        - lang (str): The original lanuage of the text.
        - targets (list): List of lanuages you want to translate to.

    Returns:
        list: List of translated texts with their target languages.

    Raises:
        OSError: Port of translating library in use.
    """
    responses:list = []

    for target in targets:

        try:
            translation = translate.translate(text, lang, target)
        except AttributeError:
            responses.append({"Error": f"Either of the languages may not be available, {lang, target}"})
            continue
        
        responses.append({"text": translation, "lang": target})

    return responses
