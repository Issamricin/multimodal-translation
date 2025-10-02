import io
import json
import os
import subprocess
import wave
from pathlib import Path

from vosk import KaldiRecognizer, Model, SetLogLevel

from multimodaltranslation.text.translate import send_text

SetLogLevel(-1)



def convert_to_wav_bytes(audio_bytes:bytes)-> io.BytesIO:
    """
    Converts the different audio types into wav (using ffmpeg) which is needed by our model.

    Args:
        - audio_bytes (bytes): The audio file in bytes.

    Returns:
        io.BytesIO: The converted audio file. 

    Raises:
        RuntimeError: If the conversion process fails.
    """

    input_file = "temp" # A temporary file to store our audio in.
    with open(input_file, "wb") as f:
        f.write(audio_bytes)  # Storing the audio bytes in the temporary file so we can use the ffmpeg command on it.

    command = [ # This command converts the audio into wav form with the specified settings.
        "ffmpeg",
        "-i", input_file,
        "-ar", "16000",     # resample 16kHz
        "-ac", "1",         # mono
        "-f", "wav",        # output format WAV
        "pipe:1"            # write to stdout instead of file, This way we don't create unnecessary files.
    ]

    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True) # Run the command and catch the stdout
    except subprocess.CalledProcessError :
        os.remove(input_file)
        raise RuntimeError("ffmpeg conversion failed")

     # Delete the temporary file.
    os.remove(input_file)
    # Wrap bytes in BytesIO so it behaves like a file.
    wav_file = io.BytesIO(proc.stdout) # Save the stdout that was in the pipe into a file.
    return wav_file


def audio_to_text(audio_bytes:bytes, model:str) -> str:
    """
    Converts the audio files into text. 

    Args:
        - audio_bytes (bytes): The bytes of the audio file.
        - model (str): The path to the correct model as a string.

    Returns:
        str : The transcription of the audio. 

    Raises:
        RuntimeError: If the conversion of the audio file to wav type failed.
    """

    try:
        wav_buffer = convert_to_wav_bytes(audio_bytes)
    except RuntimeError as e:
        raise RuntimeError(e)


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

    result = str(results[0]["text"])
    return result


def translate_audio(audio_bytes:bytes, lang:str, targets:list, libport:int = 5000) -> list:
    """
    Calls the audio_to_text to convert the audio into a trancsiped text. Then translates it into desired langs using the senf_text() method.

    Args:
        - audio_bytes (bytes): The bytes of the audio file.
        - lang (str): The original language of the audio.
        - targets (list): A list of lanuages desired for translation.

    Returns:
        list : List of translated texts with the target language.

    Raises:
        RuntimeError: If the conversion of the audio file to wav type failed.

    """
    script_dir = Path(__file__).resolve()
    model_path = str(script_dir.parent.parent.parent.parent)

    if lang == "en": #could be match: case: but the tox is failling since match was introduced in python 3.10, tox is testing on 3.9
        model_path = os.path.join(model_path,"models","vosk-model-small-en-us-0.15")
    elif lang == "zh":
        model_path = os.path.join(model_path,"models","vosk-model-small-cn-0.22")
    elif lang == "fr":
        model_path = os.path.join(model_path,"models","vosk-model-small-fr-0.22")
    else:
        return [{"Error": f"The language {lang} is not available"}]

    try:
        text = audio_to_text(audio_bytes, model_path)
    except RuntimeError as e:
        return [{"Error":str(e)}]

    translated_text = send_text(text, lang, targets, libport)
    return translated_text
