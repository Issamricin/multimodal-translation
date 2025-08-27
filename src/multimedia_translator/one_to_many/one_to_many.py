from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
import json

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
    
    def do_POST(self):
        content_type = self.headers.get("Content-Type", "")
        
        if "application/json" not in content_type:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Content-Type must be application/json"}')
            return
        
        if self.path == "/title":
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            title = data['title']
            lang = data['lang']
            targets = data['targets']

            responses = []

            for target in targets:
                payload = {
                    "q": title,
                    "source": lang,
                    "target": target 
                    }
                
                if lang not in LANGUAGE:
                
                    response = {lang: "This langauge is not available"}
                    response_bytes = json.dumps(response).encode("utf-8")

                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(response_bytes)))
                    self.end_headers()

                    self.wfile.write(response_bytes)

                if target not in LANGUAGE:

                    response = {target: "This langauge is not available"}
                    response_bytes = json.dumps(response).encode("utf-8")

                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(response_bytes)))
                    self.end_headers()

                    self.wfile.write(response_bytes)

                conn = http.client.HTTPConnection("localhost", 5000)
                json_data = json.dumps(payload)

                headers = {"Content-Type": "application/json"}
                conn.request("POST", "/translate", body=json_data, headers=headers)

                response = conn.getresponse()
                response_body = response.read()
                data = json.loads(response_body)

                responses.append({"title": data["translatedText"], "lang": target})

            responses_bytes = json.dumps(responses).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        elif self.path == "/body":
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
                return

            title = data['title']
            body = data['body']
            lang = data['lang']
            targets = data['targets']

            responses = []

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
               
                if lang not in LANGUAGE:
                
                    response = {lang: "This langauge is not available"}
                    response_bytes = json.dumps(response).encode("utf-8")

                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(response_bytes)))
                    self.end_headers()

                    self.wfile.write(response_bytes)

                if target not in LANGUAGE:

                    response = {target: "This langauge is not available"}
                    response_bytes = json.dumps(response).encode("utf-8")

                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(response_bytes)))
                    self.end_headers()

                    self.wfile.write(response_bytes)

                conn = http.client.HTTPConnection("localhost", 5000)
                json_data_t = json.dumps(payload_t)

                headers = {"Content-Type": "application/json"}
                conn.request("POST", "/translate", body=json_data_t, headers=headers)

                response = conn.getresponse()
                response_t = response.read()
                data_t = json.loads(response_t)

                json_data_b = json.dumps(payload_b)
                conn.request("POST", "/translate", body=json_data_b, headers=headers)

                response = conn.getresponse()
                response_b = response.read()
                data_b = json.loads(response_b)

                responses.append({"title": data_t["translatedText"], "body": data_b["translatedText"], "lang": target})

            responses_bytes = json.dumps(responses).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)

        else:

            response = {"Error": "Wrong path (available: /title /body)"}

            responses_bytes = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(responses_bytes)))
            self.end_headers()
            self.wfile.write(responses_bytes)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MyHandler)
    server.serve_forever()