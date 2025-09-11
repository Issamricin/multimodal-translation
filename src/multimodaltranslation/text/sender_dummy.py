# This is a simulation for sending a request to the server. And getting a response back.
"""
This is a script to test the server. 
It sends dummy data to the server to see the different responses.
"""
import pprint

import requests

def translate_text(my_object:dict) -> None:
    response = requests.post("http://localhost:8000/text", json=my_object, headers={"Content-Type": "application/json"})
    pprint.pprint(response.json())


my_object = {"text": "Hello", "lang": "en", "targets": ["it","eds"]}
translate_text(my_object)
