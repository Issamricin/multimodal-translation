from multimodaltranslation.text.translate import translate_text


def test_send_text_valid():
    answer = translate_text("Hello", "en", ["es"])
    assert answer == [{"text":"Hola.", "lang":"es"}]

def test_send_text_invalid_lang():
    answer = translate_text("Hello", "enf", ["es"])
    assert answer == [{'Error': "Either of the languages may not be available, ('enf', 'es'). Install the argos text-to-text translating language not only the vosk model."}]

def test_send_text_invalid_type():
    answer = translate_text("hello", 23, ['es'])
    assert answer == [{"Error": "Either of the languages may not be available, (23, 'es'). Install the argos text-to-text translating language not only the vosk model."}]

def test_send_text_invalid_target():
    answer = translate_text("Hello", "en", ['es','frr',12])
    assert answer == [{"text":"Hola.", "lang":"es"}, {"Error": "Either of the languages may not be available, ('en', 'frr'). Install the argos text-to-text translating language not only the vosk model."}, {"Error": "Either of the languages may not be available, ('en', 12). Install the argos text-to-text translating language not only the vosk model."}]

