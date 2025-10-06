import sys

from multimodaltranslation.main import cli_translate, main

import warnings


def test_main_translation(monkeypatch, capsys):

    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")

    test_args = ["translator", "-o", "en", "-t", "es", "-txt", "Hello"]
    monkeypatch.setattr(sys, "argv", test_args)

    main()  # should call cli_translate and print
    captured = capsys.readouterr()
    assert "[{'text': 'Hola.', 'lang': 'es'}]" in captured.out

def test_cli_translate():
    assert cli_translate('en', ['es'], text = ['Hello'], file=None) == [{'lang': 'es', 'text': 'Hola.'}]


def test_cli_translate_NoText(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Hello")
    answer = cli_translate('en', ['es'], text = None, file=None)

    assert answer == [{'lang': 'es', 'text': 'Hola.'}]


def test_cli_translate_NoLang(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "en")
    answer = cli_translate(None, ['es'], text = ["Hello"], file=None)

    assert answer == [{'lang': 'es', 'text': 'Hola.'}]


def test_cli_translate_NoTarget(monkeypatch):
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")
    monkeypatch.setattr("builtins.input", lambda _: "es fr")
    answer = cli_translate('en', None, text = ["Hello"], file=None)
    
    assert answer == [{'lang': 'es', 'text': 'Hola.'},{'lang': 'fr', 'text': 'Bonjour.'}]


def test_cli_translate_file():
    warnings.filterwarnings("ignore", category=FutureWarning, module="stanza.models.tokenize.trainer")
    answer = cli_translate('en', ['es'], text = None, file="audio_files/sample1/english.wav")
    
    assert answer == [{'lang': 'es', 'text': 'uno dos tres'}]