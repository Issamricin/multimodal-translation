import os
import warnings
from pathlib import Path

from appdirs import user_data_dir

from multimodaltranslation.audio.translate import (
    audio_to_text,
    translate_audio,
)


def test_audio_to_text():
    script_dir = Path(__file__).resolve()

    model_path = str(Path(user_data_dir("multimodaltranslator")) / "models" / "vosk-model-small-en-us-0.15")

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()  

    text = audio_to_text(audio_bytes, model_path)
    assert text == "one two three"



def test_en_translate_audio():
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")
    script_dir = Path(__file__).resolve()

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read() 

    translation = translate_audio(audio_bytes, "en", ["fr"])

    assert translation[0]['text'] == "un deux trois"

def test_zh_translate_audio():
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")
    script_dir = Path(__file__).resolve()

    audio_path = str(script_dir.parent.parent.parent)
    audio_path = os.path.join(audio_path,"audio_files","sample1","chinese.flac")

    with open(audio_path, "rb") as f:
        audio_bytes = f.read() 

    translation = translate_audio(audio_bytes, "zh", ["fr"])

    assert translation[0]['text'] == "Nos propres pieds."

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

    assert translation[0]['Error'] == "language 'endds' is not available"
