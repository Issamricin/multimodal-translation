import os
import threading
from http.server import HTTPServer
from pathlib import Path

import pytest

from multimodaltranslation.audio.translate import (
    audio_to_text,
    translate_audio,
)
from multimodaltranslation.libretranslate_server import Libretranslate_Server
from multimodaltranslation.server import MyHandler


@pytest.fixture(scope="module", autouse=True)
def start_server():
    lib_server = Libretranslate_Server()
    lib_server.start_libretranslate_server(libport=5000)

    server = HTTPServer(("localhost", 8000), MyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon=True #So python can still shutdown the server cleanly if we forgot to.
    thread.start()
    yield # means do the tests and finish them then come back and continue after the yield.
    lib_server.stop_libretranslate_server()
    server.shutdown()
    thread.join()

def test_audio_to_text():
    script_dir = Path(__file__).resolve()

    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()  

    text = audio_to_text(audio_bytes, model_path)
    assert text == "one two three"



def test_en_translate_audio():
    script_dir = Path(__file__).resolve()

    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read() 

    translation = translate_audio(audio_bytes, "en", ["fr"])

    assert translation[0]['text'] == "un deux trois"

def test_zh_translate_audio():
    script_dir = Path(__file__).resolve()

    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"models","vosk-model-small-cn-0.22")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","chinese.flac")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read() 

    translation = translate_audio(audio_bytes, "zh", ["fr"])

    assert translation[0]['text'] == "Nos propres pieds"

def test_invalidAudio_translate_audio():
    script_dir = Path(__file__).resolve()

    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = b"2323" + f.read() + b"121412441"

    translation = translate_audio(audio_bytes, "en", ["fr"])

    assert translation[0]['Error'] == "ffmpeg conversion failed"


def test_invalidLang_translate_audio():
    script_dir = Path(__file__).resolve()

    model_path = str(script_dir.parent.parent.parent)
    model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    translation = translate_audio(audio_bytes, "endds", ["fr"])

    assert translation[0]['Error'] == "The language endds is not available"
