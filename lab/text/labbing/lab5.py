import requests

url = "http://localhost:5000/translate"  # or the hosted server
payload = {
    "q": "Hello, this is testing.",
    "source": "en",
    "target": "fr" #choose the lang you want to translate to
}

payload2 = {
    "q": "Hello, this is testing.",
    "source": "en",
    "target": "it" #choose the lang you want to translate to
}

payload3 = {
    "q": "Hello, this is testing.",
    "source": "en",
    "target": "es" #choose the lang you want to translate to
}

lis = [payload,payload2,payload3]

for i in lis:
    response = requests.post(url, data=i)
    print(response.json())
