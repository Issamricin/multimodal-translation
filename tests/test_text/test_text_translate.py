from multimodaltranslation.text.translate import translate_text


def test_send_text_valid():
    answer = translate_text("Hello", "en", ["es"])
    assert answer == [{"text":"Hola.", "lang":"es"}]

def test_send_text_invalid_lang():
    answer = translate_text("Hello", "enf", ["es"])
    assert answer == [{'text': '', 'lang': 'es'}]

def test_send_text_invalid_type():
    answer = translate_text("hello", 23, ['es'])
    assert answer == [{'text': '', 'lang': 'es'}]

def test_send_text_invalid_target():
    answer = translate_text("Hello", "en", ['es','frr',12])
    assert answer == [{"text":"Hola.", "lang":"es"}, {'text': '', 'lang': 'frr'}, {'text': '', 'lang': 12}]

