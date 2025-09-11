import requests

url = "http://localhost:8000/audio"

# 'file' is the file upload, 'language' and 'targets' are strings
with open("audio_files/sample1/english.wav", "rb") as f:
    audio_bytes = f.read()
audio_str = audio_bytes.hex()
files = {
    "audio": audio_str,
    "lang":"en",
    "targets": ["fr","en"]  
}

response = requests.post(url, json=files)
print(response.text)