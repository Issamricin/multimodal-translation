"""
This is the free google recognizer. It only lisens to english audio, if you try chinese it says forbidden. 
"""
import os
from pathlib import Path

import speech_recognition as sr


def extract_text_from_audio(file:str) -> str:
    audio = sr.AudioData.from_file(file)
    recognizer = sr.Recognizer()

    try:
        text = recognizer.recognize_google(audio,"zh-CN")
        print("Sphinx thinks you said " + text)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return
    except sr.RequestError as err:
        print(f"Sphinx error; {err}")
        return

    return text

def main() -> None:

    audio_file = str(Path(__file__).resolve().parents[2].joinpath("audio_files")) + \
        os.sep + 'sample1' + os.sep + "chinese.flac"
    print(extract_text_from_audio(audio_file))


if __name__ == "__main__":
    main()
