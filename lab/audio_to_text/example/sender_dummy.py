import os
from pathlib import Path

import requests

url = "http://localhost:8000/audio"

script_dir = Path(__file__).resolve()
AUDIO_PATH = str(script_dir.parent.parent.parent.parent)
AUDIO_PATH = os.path.join(AUDIO_PATH,"audio_files","sample1","english.wav")

with open(AUDIO_PATH, "rb") as f:
    AUDIO_BYTES = f.read()    

audio_str = AUDIO_BYTES.hex()
files = {
    "audio": audio_str,
    "lang":"en",
    "targets": ["fr","es"]
}

RESPONSE = requests.post(url, json=files)
print(RESPONSE.text)
