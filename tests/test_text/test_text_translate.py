import pytest

from multimodaltranslation.libretranslate_server import Libretranslate_Server
from multimodaltranslation.text.translate import send_text


@pytest.fixture(scope="module", autouse=True)
def start_server():
    lib_server = Libretranslate_Server()
    lib_server.start_libretranslate_server(libport=5000)
    yield # means do the tests and finish them then come back and continue after the yield.
    lib_server.stop_libretranslate_server()

def test_send_text_valid():
    answer = send_text("Hello", "en", ["es"], 5000)
    assert answer == [{"text":"Hola", "lang":"es"}]

def test_send_text_invalid_lang():
    answer = send_text("Hello", "enf", ["es"], 5000)
    assert answer == [{"Error": "This language is not available, enf"}]

def test_send_text_invalid_type():
    answer = send_text("hello", 23, ['es'], 5000)
    assert answer == [{"Error": "Language should be string not <class 'int'>"}]

def test_send_text_invalid_target():
    answer = send_text("Hello", "en", ['es','frr',12], 5000)
    assert answer == [{"text":"Hola", "lang":"es"}, {"Error":"This language is not available, frr"}, {"Error": "Target language should be string not <class 'int'>"}]

