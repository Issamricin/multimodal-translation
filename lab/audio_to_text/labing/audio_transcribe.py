# copied from https://github.com/Uberi/speech_recognition/tree/master/examples
# only one language model English see:
# https://github.com/Uberi/speech_recognition/tree/master/speech_recognition/pocketsphinx-data/en-US
# obtain path to "english.wav" in the same folder as this script
from os import path
from pathlib import Path

import speech_recognition as sr


# recognize speech using Sphinx; we don't need any registration or api-key
# English
def translate(file:str)->None:
    audio = sr.AudioData.from_file(file)
    r = sr.Recognizer()
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print(f"Sphinx error; {e}")

def main()-> None:
    # English
    audio_file = str(Path(__file__).resolve().parents[3].joinpath("audio_files")) + \
        path.sep + 'sample1' + path.sep + "english.wav"
    translate(audio_file)

    audio_file = str(Path(__file__).resolve().parents[3].joinpath("audio_files")) + \
        path.sep + 'sample2' + path.sep + "test01_20s.wav"
    translate(audio_file)

     # 34210__acclivity__i-am-female.wav 23.7 MB takes 1 minutes and 30 sec.
    audio_file = str(Path(__file__).resolve().parents[3].joinpath("audio_files")) + \
        path.sep + 'sample2' + path.sep + "34210__acclivity__i-am-female.wav"
    translate(audio_file)

     # Chinese has no model
    audio_file = str(Path(__file__).resolve().parents[3].joinpath("audio_files")) + \
        path.sep + 'sample1' + path.sep + "chinese.flac"
    translate(audio_file)


if __name__ == "__main__":
    main()
