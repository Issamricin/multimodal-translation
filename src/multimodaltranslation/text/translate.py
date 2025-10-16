import os
import warnings

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Hide GPUs
os.environ["STANZA_USE_GPU"] = "False"   # Force Stanza CPU
           

# Now import and use Argos Translate
import argostranslate.translate
from argostranslate import translate

warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")


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
            responses.append({"Error": f"Either of the languages may not be available, {lang, target}. Install the argos text-to-text translating language not only the vosk model."})
            continue

        responses.append({"text": translation, "lang": target})

    return responses
