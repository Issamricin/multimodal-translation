import io
import json
import subprocess
import wave

from vosk import KaldiRecognizer, Model


def convert_to_wav_bytes(input_file):
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
    return io.BytesIO(proc.stdout)

# Example usage
wav_buffer = convert_to_wav_bytes("audio_files/sample1/chinese.flac")

# Open with wave module (or pass to vosk directly)
wf = wave.open(wav_buffer, "rb")

# Load French model (change to "model-cn" for Chinese)
model = Model("models/vosk-model-small-cn-0.22")

# Create recognizer
rec = KaldiRecognizer(model, wf.getframerate())

# Process audio
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())

# Final result
final = json.loads(rec.FinalResult())
print("Final:", final["text"])
