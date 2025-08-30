import threading
import requests
import pytest
from http.server import HTTPServer
from multimodaltranslation.text.translate import MyHandler

#Rewan you have to fill the empty test methods. Leave the functioning complete ones.

@pytest.fixture(scope="module", autouse=True)
def start_server():
    server = HTTPServer(("localhost", 8000), MyHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon=True #So python can still shutdown the server cleanly if we forgot to.
    thread.start()
    yield # means do the tests and finish them then come back and continue after the yield.
    server.shutdown()
    thread.join()

def test_title_translate_valid():

    #This is testing the /title path with valid input
    payload = {"title":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/title",json=payload)

    assert respone.status_code == 200
    data = respone.json()
    assert isinstance(data,list)
    assert data[0]["title"] == "Hola"


def test_body_translate_valid():

    #Rewan do the same for the /body path
    pass


def test_title_translate_invalid_type():

    #This is testing the /title path for invalid content type
    payload = {"title":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/title",data=payload, headers={"Content-Type":"text/plain"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["error"] == "Content-Type must be application/json"


def test_body_translate_invalid_type():

    #rewan will do the same for the /body path
    pass


def test_title_invalid_json():

    #This is testing the /title path for invalid json
    respone = requests.post("http://localhost:8000/title",data="{bad json", headers={"Content-Type":"application/json"},)

    assert respone.status_code == 400
    data = respone.json()
    assert data["error"] == "Invalid JSON"


def test_body_invalid_json():

    #rewan will do the same for the /body path
    pass


# Test for invalid keys in the json data (payload)
def test_title_invalid_keys():
    pass

def test_body_invalid_keys():
    pass


def test_title_invalid_lang():

    #This is testing the /title path for unavailable source langauge
    payload = {"title":"Hello", "lang":"no langauge", "targets":["es"]}
    respone = requests.post("http://localhost:8000/title",json=payload)

    assert respone.status_code == 400
    data = respone.json()
    assert data['no langauge'] == "This langauge is not available"


def test_body_invalid_lang():
    pass


#do the same test for the target langauge (the one we want to translate to)
def test_title_invalid_target():
    pass

def test_body_invalid_target():
    pass


def test_wrong_path():

    #This is testing wrong path given
    payload = {"title":"Hello", "lang":"en", "targets":["es"]}
    respone = requests.post("http://localhost:8000/wrong",json=payload)

    assert respone.status_code == 400
    data = respone.json()
    assert data['error'] == "wrong path (available: 1-/title 2-/body)"
