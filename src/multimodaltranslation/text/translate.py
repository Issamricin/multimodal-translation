import http.client
import json
from multimodaltranslation.libretranslate_server import Libretranslate_Server

LANGUAGE = [
     "en",
     "it",
     "es",
     "fr",
     "zh"
    ]

def translate_text(text:str, lang:str, targets:list, libport = 5000) -> list:
    """
    Translates the text sent to it into the desired languages (targets).

    Args:
        - text (str): The text you want to translate.
        - lang (str): The original lanuage of the text.
        - targets (list): List of lanuages you want to translate to.

    Returns:
        list: List of translated texts with their target languages.
    """
    try:
        lib_server = Libretranslate_Server()
        lib_server.start_libretranslate_server(libport=libport)
    except Exception as e:
        lib_server.stop_libretranslate_server()
        return [f"-{libport} Port might be taken!"]

    translation = send_text(text, lang, targets, libport)
    
    lib_server.stop_libretranslate_server()
    return translation

def send_text(text:str, lang:str, targets:list, libport ) -> list:

            responses:list = []

            if lang not in LANGUAGE:
                if not isinstance(lang, str):
                    responses.append({"Error": f"{lang} should be string not {type(lang)}"})
                else:
                    responses.append({"Error": f"This language is not available, {lang}"})

                return responses

            for target in targets:
                payload = {
                    "q": text,
                    "source": lang,
                    "target": target 
                    }


                if target not in LANGUAGE:
                    if not isinstance(target, str):
                        responses.append({"Error": f"{target} should be string not {type(target)}"})
                    else:
                        responses.append({"Error": f"This language is not available, {target}"})

                    continue

                conn = http.client.HTTPConnection("localhost", libport)
                json_data = json.dumps(payload)

                headers = {"Content-Type": "application/json"}
                try:
                    conn.request("POST", "/translate", body=json_data, headers=headers)
                except Exception as e:
                     return e

                translation = conn.getresponse()
                response_body = translation.read()
                data = json.loads(response_body)

                responses.append({"text": data["translatedText"], "lang": target})

            return responses
