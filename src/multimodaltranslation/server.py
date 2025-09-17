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
            self.wfile.write(b'{"Error": "Content-Type must be application/json"}')
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
                self.wfile.write(b'{"Error": "Invalid JSON"}')
                return

            try:
                text = str(data['text'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"Error": "Invalid keys", "keys": "text, lang, targets"}')
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
                self.wfile.write(b'{"Error": "Invalid JSON"}')
                return

            try:
                audio = str(data['audio'])
                lang = data['lang']
                targets = data['targets']
            except KeyError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"Error": "Invalid keys", "keys": "audio, lang, targets"}')
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

            response = {"Error": "Wrong path (available: /text, /audio)"}

            responses_bytes = json.dumps(response).encode("utf-8")

            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)
            return
