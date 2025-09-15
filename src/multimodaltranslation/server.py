import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from multimodaltranslation.audio.translate import translate_audio
from multimodaltranslation.text.translate import translate_text

LANGUAGE = [
     "en",
     "it",
     "es",
     "fr",
     "zh"
    ]


url = "http://localhost:5000/translate" #for libreTranslate

class MyHandler(BaseHTTPRequestHandler):
    """
    Handles the calls for the server. You use this class to create a server on a specific port.        
    
    Example:
        >>> server = HTTPServer(("localhost", 8000), MyHandler)
        >>> server.serve_forever()
    """
    print("Starting server ...")

    def do_POST(self) -> None :
        """
        Handles the different routes. For /text it will translate the text into the desired languages. 
        For /audio it will transcript and translate the audio into the desired languages.

        Args:
            - self

        Returns:
            - None
        """

        content_type = self.headers.get("Content-Type", "")

        if "application/json" not in content_type:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Content-Type must be application/json"}')
            return

        if self.path == "/text": # route(/title)
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
                text = str(data['text'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid keys", "keys": "text, lang, targets"}')
                return

            if check_lang(self, lang, LANGUAGE):
                return

            responses = translate_text( text, lang, targets)

            responses_bytes = json.dumps(responses).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        elif self.path == "/audio":
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
                audio = str(data['audio'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid keys", "keys": "audio, lang, targets"}')
                return

            if check_lang(self, lang, LANGUAGE):
                return

            audio_bytes = bytes.fromhex(audio)

            responses = translate_audio(audio_bytes,  lang, targets)

            responses_bytes = json.dumps(responses, ensure_ascii=False).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        else:

            response = {"error": "wrong path (available: /text, /audio)"}

            responses_bytes = json.dumps(response).encode("utf-8")

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)
            return

def check_lang(self:MyHandler, lang:str, langs:list) -> bool:
            """
            Checks if the original language of the /text or /audio is available in the list of languages or not.

            Args:
                - self (MyHandler): The handler class.
                - lang (str): The language you want to check.
                - langs (list): The list of the languages that are available.

            Returns:
                - bool: True or False
            """
            if lang not in langs:

                if not isinstance(lang, str):
                    response = {str(lang): f"Type error: Should be string not {type(lang)}"}
                else:
                    response = {lang: "Error, this langauge is not available"}

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
    port = 8000
    server = HTTPServer(("localhost", port), MyHandler)
    print(f"server started on localhost port: {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nClosing server...")
