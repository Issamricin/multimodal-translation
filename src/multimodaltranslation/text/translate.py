import http.client
import json

LANGUAGE = [
     "en",
     "it",
     "es",
     "fr",
     "zh"
    ]


def translate_text(text:str, lang:str, targets:list) -> list:
            """
            Translates the text sent to it into the desired languages (targets).

            Args:
                - text (str): The text you want to translate.
                - lang (str): The original lanuage of the text.
                - targets (list): List of lanuages you want to translate to.

            Returns:
                - list: List of translated texts with their target languages.
            """

            responses:list = []
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
                        responses.append({"Error": f"This language is not available: {target}"})

                    continue


                conn = http.client.HTTPConnection("localhost", 5000)
                json_data = json.dumps(payload)

                headers = {"Content-Type": "application/json"}
                conn.request("POST", "/translate", body=json_data, headers=headers)

                translation = conn.getresponse()
                response_body = translation.read()
                data = json.loads(response_body)

                responses.append({"text": data["translatedText"], "lang": target})

            return responses
