import warnings

from argostranslate import translate
import logging
import time
import concurrent.futures

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
    responses:list[dict[str,str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for target in targets:
            result = executor.submit(_do_translate,text, lang, target)
            responses.append(result) 
        data = concurrent.futures.as_completed(responses)
        results:list[dict[str,str]] = []
        for _ in concurrent.futures.as_completed(data):
            results.append(_.result())
        t2 = time.perf_counter()
        delta = str(t2-t1)
        logger.info(f'Transalation from {lang} to {targets} took {delta} seconds')
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
    