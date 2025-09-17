import requests
from pathlib import Path
import os

url = "http://localhost:8000/audio"

script_dir = Path(__file__).resolve()
model_path = str(script_dir.parent.parent.parent.parent)
model_path = os.path.join(model_path,"audio_files","sample1","english.wav")

with open(model_path, "rb") as f:
    audio_bytes = f.read()    

audio_str = audio_bytes.hex()
files = {
    "audio": audio_str,
    "lang":"en",
    "targets": ["fr","es"]  
}

response = requests.post(url, json=files)
print(response.text)
