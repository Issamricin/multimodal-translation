import threading
import warnings
from http.server import HTTPServer

import pytest
import requests

from multimodaltranslation.server import MyHandler


@pytest.fixture(scope="module", autouse=True)
def start_server():
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")
    server = HTTPServer(("localhost", 8000), MyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon=True #So python can still shutdown the server cleanly if we forgot to.
    thread.start()
    yield # means do the tests and finish them then come back and continue after the yield.
    server.shutdown()
    thread.join()

def test_text_translate_valid():

    #This is testing the /text path with valid input
    payload = {"text":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/text",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert isinstance(data,list)
    assert data[0]["text"] == "Hola."


def test_text_translate_invalid_type():

    #This is testing the /text path for invalid content type
    payload = {"text":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/text",data=payload, headers={"Content-Type":"text/plain"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Content-Type must be application/json"


def test_text_invalid_json():

    #This is testing the /text path for invalid json
    respone = requests.post("http://localhost:8000/text",data="{bad json", headers={"Content-Type":"application/json"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Invalid JSON"


# Test for invalid keys in the json data (payload)
def test_text_invalid_keys():

    respone = requests.post("http://localhost:8000/text",json={"texts":"Hello", "langs":"en", "targets":["es"]}, headers={"Content-Type":"application/json"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Invalid keys" 
    assert data["keys"] == "text, lang, targets"


def test_text_invalid_lang():

    #This is testing the /text path for unavailable source langauge
    payload = {"text":"Hello", "lang":"no language", "targets":["es"]}
    respone = requests.post("http://localhost:8000/text",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert data[0]['Error'] == "Either of the languages may not be available, ('no language', 'es'). Install the argos text-to-text translating language."

def test_text_invalid_target():

    #This is testing the /text path for unavailable target langauge
    payload = {"text":"Hello", "lang":"en", "targets":["bbc"]}
    respone = requests.post("http://localhost:8000/text",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert data[0]['Error'] == "Either of the languages may not be available, ('en', 'bbc'). Install the argos text-to-text translating language."


def test_wrong_path():

    #This is testing wrong path given
    payload = {"text":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/wrong",json=payload)

    assert respone.status_code == 400
    data = respone.json()
    assert data['Error'] == "Wrong path (available: /text, /audio)"
