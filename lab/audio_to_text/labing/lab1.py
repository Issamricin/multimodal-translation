"""
This is sphinx recognizer. It only lisens to english audio.
"""
import os
import pprint
from pathlib import Path

import requests
import speech_recognition as sr


def extract_text_from_audio(file:str) -> str:
    audio = sr.AudioData.from_file(file)
    r = sr.Recognizer()

    try:
        text = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + text)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return
    except sr.RequestError as e:
        print(f"Sphinx error; {e}")
        return

    return text

def translate_to_text(file, source="en", targets=None):
    if targets is None:
        targets = ["it","es"]

    text = extract_text_from_audio(file)

    my_object = {"title": text, "lang": source, "targets": targets}

    response = requests.post("http://localhost:8000/title", json=my_object, \
                             headers={"Content-Type": "application/json"}, timeout=10)
    pprint.pprint(response.json())


def main() -> None:

    audio_file = str(Path(__file__).resolve().parents[2].joinpath("audio_files")) + os.sep + \
    'sample1' + os.sep + "english.wav"

    translate_to_text(audio_file)


if __name__ == "__main__":
    main()
