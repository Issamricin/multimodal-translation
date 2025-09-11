from vosk import Model, KaldiRecognizer
import wave
import json
import subprocess
import io
import os
from pathlib import Path

from multimodaltranslation.text.translate import translate_text

def convert_to_wav_bytes(audio_bytes):
    input_file = f"temp"
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


def audio_to_text(audio_bytes, model):
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

    return results[0]["text"]


def translate_audio(audio_bytes, lang, targets) -> list:

    script_dir = Path(__file__).resolve()
    model_path = script_dir.parent.parent.parent.parent

    match lang:
        case "en":
            model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")
        case "zh":
            model_path = os.path.join(model_path,"models","vosk-model-small-cn-0.22")
        case "fr":
            model_path = os.path.join(model_path,"models","vosk-model-small-fr-0.22")
        case default:
            return {"error": f"The language {lang} is not available"}


    text = audio_to_text(audio_bytes, model_path)
    translated_text = translate_text(text, lang, targets)

    return translated_text
