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

def translate_text(text:str, lang:str, targets:list, libport:int = 5000) -> list:
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
    try:
        lib_server = Libretranslate_Server()
        lib_server.start_libretranslate_server(libport=libport)
    except OSError:
        lib_server.stop_libretranslate_server()
        return [f"Error: Ports are in use. You can change the ports using the -lp and -ap flags. (-h for more help) -{libport}"]

    translation = send_text(text, lang, targets, libport)

    lib_server.stop_libretranslate_server()
    return translation

def send_text(text:str, lang:str, targets:list, libport:int ) -> list:
            """
            Sends the text to the translating library for translation.
            It doesn't turn the library server on itself, rather the server should be on already.

            Args:
                text (str): The text to be sent to the translating server.
                lang (str): The language of the original text.
                targets (list): The list of target languages to translate to.
                libport (int): The port of the translating library.

            Returns:
                list: List of translated texts with their target languages.

            Raises:
                Exception: If the connection to the translating library failed for any reason.
            """

            responses:list = []

            if lang not in LANGUAGE:
                if not isinstance(lang, str):
                    responses.append({"Error": f"Language should be string not {type(lang)}"})
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
                        responses.append({"Error": f"Target language should be string not {type(target)}"})
                    else:
                        responses.append({"Error": f"This language is not available, {target}"})

                    continue

                conn = http.client.HTTPConnection("localhost", libport)
                json_data = json.dumps(payload)

                headers = {"Content-Type": "application/json"}
                try:
                    conn.request("POST", "/translate", body=json_data, headers=headers)
                except Exception as e:
                     return [e]

                translation = conn.getresponse()
                response_body = translation.read()
                data = json.loads(response_body)

                responses.append({"text": data["translatedText"], "lang": target})

            return responses
