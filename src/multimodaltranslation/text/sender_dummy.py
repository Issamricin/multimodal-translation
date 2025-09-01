# This is a simulation for sending a request to the server. And getting a response back.

import pprint

import requests


def translate_title(my_object:dict) -> None:
    response = requests.post("http://localhost:8000/title", json=my_object, headers={"Content-Type": "application/json"})
    pprint.pprint(response.json())

def translate_body(my_object:dict) -> None:
    response = requests.post("http://localhost:8000/body", json=my_object, headers={"Content-Type": "application/json"})
    pprint.pprint(response.json())


my_object = {"title": "Hello", "body": "this is the body", "lang": "en", "targets": ["it","es"]}
translate_body(my_object)


#my_object = {"title": "hello","lang": "en", "targets": ["it","es"]}
#translate_title(my_object)
