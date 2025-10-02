import os
from pathlib import Path

import requests

url = "http://localhost:8000/audio"

script_dir = Path(__file__).resolve()
audio_path = str(script_dir.parent.parent.parent.parent)
audio_path = os.path.join(audio_path,"audio_files","sample1","english.wav")

with open(audio_path, "rb") as f:
    audio_bytes = f.read()    

audio_str = audio_bytes.hex()
files = {
    "audio": audio_str,
    "lang":"en",
    "targets": ["fr","es"]  
}

response = requests.post(url, json=files)
print(response.text)
