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
            Handles the /title route. It translates the title into the desired output.

            Args:
                - self (MyHandler): The handler class.
                - title (str): The title you want to translate.
                - lang (str): The original lanuage of the title.
                - targets (list): List of lanuages you want to translate the title to.
                - responses (list): The list containing the responses of different languages and errors. 

            Returns:
                - None

            Example:

                >>> responses = []
                >>> translate_title(self, title, lang, targets, responses)
                >>> responses_bytes = json.dumps(response).encode("utf-8")
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
                        responses.append({str(target): f"Type error, should be string not {type(target)}"})
                    else:
                        responses.append({target: "This langauge is not available"})
                    
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
