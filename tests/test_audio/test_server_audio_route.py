import os
import threading
from http.server import HTTPServer
from pathlib import Path

import pytest
import requests

from multimodaltranslation.server import MyHandler


@pytest.fixture(scope="module", autouse=True)
def start_server():
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")

    server = HTTPServer(("localhost", 8000), MyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon=True #So python can still shutdown the server cleanly if we forgot to.
    thread.start()
    yield # means do the tests and finish them then come back and continue after the yield.
    server.shutdown()
    thread.join()

def test_audio_translate_valid():
    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"audio_files","sample1","english.wav")

    with open(model_path, "rb") as f:
        audio_bytes = f.read()    

    audio_str = audio_bytes.hex()

    payload = {"audio":audio_str, "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/audio",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert isinstance(data,list)
    assert data[0]["text"] == "uno dos tres"


def test_audio_translate_invalid_type():
    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"audio_files","sample1","english.wav")

    with open(model_path, "rb") as f:
        audio_bytes = f.read()    

    audio_str = audio_bytes.hex()

    payload = {"audio":audio_str, "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/audio",data=payload, headers={"Content-Type":"text/plain"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Content-Type must be application/json"


def test_audio_invalid_json():

    respone = requests.post("http://localhost:8000/audio",data="{bad json", headers={"Content-Type":"application/json"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Invalid JSON"


# Test for invalid keys in the json data (payload)
def test_audio_invalid_keys():

    respone = requests.post("http://localhost:8000/audio",json={"wrong":"Hello", "langs":"en", "targets":["es"]}, headers={"Content-Type":"application/json"})

    assert respone.status_code == 400
    data = respone.json()
    assert data["Error"] == "Invalid keys" 
    assert data["keys"] == "audio, lang, targets"


def test_audio_invalid_lang():
    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"audio_files","sample1","english.wav")

    with open(model_path, "rb") as f:
        audio_bytes = f.read()    

    audio_str = audio_bytes.hex()

    payload = {"audio":audio_str, "lang":"edd", "targets":["es"]}
    respone = requests.post("http://localhost:8000/audio",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert data[0]['Error'] == "language 'edd' is not available"


def test_audio_invalid_target():

    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"audio_files","sample1","english.wav")

    with open(model_path, "rb") as f:
        audio_bytes = f.read()    

    audio_str = audio_bytes.hex()

    payload = {"audio":audio_str, "lang":"en", "targets":["bbc"]}
    respone = requests.post("http://localhost:8000/audio",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert data[0]['Error'] == "Either of the languages may not be available, ('en', 'bbc'). Install the argos text-to-text translating language."

