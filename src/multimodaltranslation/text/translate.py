import http.client
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

LANGUAGE = [
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
    ]


url = "http://localhost:5000/translate" #for libreTranslate

class MyHandler(BaseHTTPRequestHandler):
    """
    Handles the calls for the server. You use this class to create a server on a specific port.
    """

    def do_POST(self) -> None :
        """
        Handles the different routes. Fot /title it will translate the title into the desired languages. 
        For /body it will translate the title and the body into the desired languages.

        Args:
            - None

        Returns:
            - None

        Example:
            >>> server = HTTPServer(("localhost", 8000), MyHandler)
            >>> server.serve_forever()
        """

        content_type = self.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Content-Type must be application/json"}')
            return

        if self.path == "/title": # route(/title)
            content_length = int(self.headers.get('Content-Length', 0)) #Could be none so we have to give a default value
            content = self.rfile.read(content_length)

            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            try:
                title = str(data['title'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid keys", "keys": "title, lang, targets"}')
                return

            if check_lang(self, lang, LANGUAGE):
                return

            responses:list = []

            translate_title(self, title, lang, targets, responses)

            responses_bytes = json.dumps(responses).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        elif self.path == "/body": #route(/body)
            content_length = int(self.headers.get('Content-Length',0)) #could return none so we give a default value of 0
            content = self.rfile.read(content_length)

            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            try:
                title = str(data['title'])
                body:str = str(data['body'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid keys", "keys": "title, body, lang, targets"}')
                return

            if check_lang(self, lang, LANGUAGE):
                return

            responses = []

            translate_body(self, title, body, lang, targets, responses)

            responses_bytes = json.dumps(responses).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        else:

            response = {"error": "wrong path (available: 1-/title 2-/body)"}

            responses_bytes = json.dumps(response).encode("utf-8")

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)
            return

def translate_title(self:MyHandler, title:str, lang:str, targets:list, responses:list) -> None:
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

            for target in targets:
                payload = {
                    "q": title,
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

                responses.append({"title": data["translatedText"], "lang": target})

def translate_body(self:MyHandler, title:str, body:str, lang:str, targets:list, responses:list) -> None:
            """
            Handles the /body route. It translates the title and the body into the desired output.

            Args:
                - self (MyHandler): The handler class.
                - title (str): The title you want to translate.
                - body (str): The body you want to translate.
                - lang (str): The original lanuage of the title.
                - targets (list): List of lanuages you want to translate the title to.
                - responses (list): The list containing the responses of different languages and errors. 

            Returns:
                - None

            Example:

                >>> responses = []
                >>> translate_body(self, title, body, lang, targets, responses)
                >>> responses_bytes = json.dumps(response).encode("utf-8")
            """
            for target in targets:
                payload_t = {
                        "q": title,
                        "source": lang,
                        "target": target #choose the lang you want to translate to
                        }
                payload_b = {
                        "q": body,
                        "source": lang,
                        "target": target #choose the lang you want to translate to
                        }

                if target not in LANGUAGE:
                    if not isinstance(target, str):
                        responses.append({str(target): f"Type error, should be string not {type(target)}"})
                    else:
                        responses.append({target: "This langauge is not available"})
                    
                    continue

                conn = http.client.HTTPConnection("localhost", 5000)
                json_data_t = json.dumps(payload_t)

                headers = {"Content-Type": "application/json"}
                conn.request("POST", "/translate", body=json_data_t, headers=headers)

                translation = conn.getresponse()
                response_t = translation.read()
                data_t = json.loads(response_t)

                json_data_b = json.dumps(payload_b)
                conn.request("POST", "/translate", body=json_data_b, headers=headers)

                translation = conn.getresponse()
                response_b = translation.read()
                data_b = json.loads(response_b)

                responses.append({"title": data_t["translatedText"], "body": data_b["translatedText"], "lang": target})

def check_lang(self:MyHandler, lang:str, langs:list) -> bool:
            """
            Checks if the original language of the title or the body is available in the list of languages or not.

            Args:
                - self (MyHandler): The handler class.
                - lang (str): The language you want to check.
                - langs (list): The list of the languages that are available.

            Returns:
                - bool: True or False
            """
            if lang not in langs:

                if not isinstance(lang, str):
                    response = {str(lang): f"Type error, should be string not {type(lang)}"}
                else:
                    response = {lang: "This langauge is not available"}

                response_bytes = json.dumps(response).encode("utf-8")
                self.send_response(400)

                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()

                self.wfile.write(response_bytes)
                return True
            else:
                return False

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MyHandler)
    server.serve_forever()
