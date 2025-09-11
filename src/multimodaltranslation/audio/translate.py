import io
import json
import os
import subprocess
import typing
import wave
from pathlib import Path

from vosk import KaldiRecognizer, Model

from multimodaltranslation.text.translate import translate_text


def convert_to_wav_bytes(audio_bytes:bytes)-> io.BytesIO:
    input_file = "temp"
    with open(input_file, "wb") as f:
        f.write(audio_bytes)
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ar", "16000",     # resample 16kHz
        "-ac", "1",         # mono
        "-f", "wav",        # output format WAV
        "pipe:1"            # write to stdout instead of file
    ]
    proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)

    # Wrap bytes in BytesIO so it behaves like a file
    os.remove(input_file)
    return io.BytesIO(proc.stdout)


def audio_to_text(audio_bytes:bytes, model:str) -> typing.Any:
    wav_buffer = convert_to_wav_bytes(audio_bytes)


    wf = wave.open(wav_buffer, "rb")

    mod = Model(model)

    # Create recognizer
    rec = KaldiRecognizer(mod, wf.getframerate())

    results = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result()))

    results.append(json.loads(rec.FinalResult()))

    result = results[0]["text"]
    return result


def translate_audio(audio_bytes:bytes, lang:str, targets:list) -> list:

    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent.parent)

    if lang == "en": #coult be match: case: but the tox is failling since match was introduced in python 3.10, tox is testing on 3.9
        model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")
    elif lang == "zh":
        model_path = os.path.join(model_path,"models","vosk-model-small-cn-0.22")
    elif lang == "fr":
        model_path = os.path.join(model_path,"models","vosk-model-small-fr-0.22")
    else:
        return [{"error": f"The language {lang} is not available"}]


    text = audio_to_text(audio_bytes, model_path)
    translated_text = translate_text(text, lang, targets)

    return translated_text
