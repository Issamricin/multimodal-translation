import requests

url = "http://localhost:5000/translate"  # or the hosted server
payload = {
    "q": "Hello, this is testing.",
    "source": "en",
    "target": "fr" #choose the lang you want to translate to
}

response = requests.post(url, data=payload)
print(response.json())
