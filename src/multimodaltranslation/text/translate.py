import warnings

from argostranslate import translate
import logging
import time
import concurrent.futures
from concurrent.futures import Future

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=FutureWarning,
                    module="stanza.models.tokenize.trainer")


def translate_text(text:str, lang:str, targets:list[str]) -> list[dict[str,str]]:
    """
    Translates the text provided into the desired languages (targets).

    Args:
        - text (str): The text you want to translate.
        - lang (str): The original language of the text.
        - targets (list): List of languages you want to translate to.

    Returns:
        list: List of translated texts with their target languages.
              In case the language is not found , it will return empty text
    """
    t1 = time.perf_counter()
    responses:list[Future] = [] # This is a list of future job
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor: # with statement allows us to use executor as a context manager also to shutdown do cleaning after the last worker thread is done
        for target in targets:
            future_result = executor.submit(_do_translate,text, lang, target) # see https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
            responses.append(future_result) # building the future list
        data = concurrent.futures.as_completed(responses) # An iterator over the given futures that yields each as it completes. it means it goes through
        results:list[dict[str,str]] = []
        for _ in concurrent.futures.as_completed(data):
            results.append(_.result())

        t2 = time.perf_counter()
        delta = str(t2-t1)
        logger.info(f'Translation from {lang} to {targets} took {delta} seconds')
        return results



def _do_translate(text:str, lang:str, target:str)->dict[str,str]:

      try:
        translated_text = translate.translate(text, lang, target)
        return {"text": translated_text, "lang":target}
      except AttributeError:
        logger.warning( f"Either of the languages may not be available, {lang, target}." \
         " Install the argos text-to-text translating language.")
        return ({"text": "", "lang" : target})



if __name__ == "__main__":
    lang = "en"
    targets = ["dk","se", "ar", "ku"]
    text = "Hi there"
    results = translate_text(text=text, lang=lang, targets=targets)
    for result in results:
        print(f"{result['text']}  {result['lang']}")
