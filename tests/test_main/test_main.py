import sys

from multimodaltranslation.main import cli_translate, main


def test_main_starts_server(monkeypatch):
    # Patch start_server so it doesn’t actually start anything
    monkeypatch.setattr("multimodaltranslation.main.start_server", lambda ap, lp: "server started")

    test_args = ["prog", "-s", "Y", "-ap", "9000", "-lp", "6000"]
    monkeypatch.setattr(sys, "argv", test_args)

    main()  # should call start_server
    # Nothing to assert since start_server was replaced, but no crash = success

def test_main_translation(monkeypatch, capsys):

    test_args = ["translator", "-o", "en", "-t", "es", "-txt", "Hello"]
    monkeypatch.setattr(sys, "argv", test_args)

    main()  # should call cli_translate and print
    captured = capsys.readouterr()
    assert "[{'text': 'Hola', 'lang': 'es'}]" in captured.out

def test_cli_translate():
    assert cli_translate('en', ['es'], text = ['Hello'], file=None) == [{'lang': 'es', 'text': 'Hola'}]


def test_cli_translate_NoText(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Hello")
    answer = cli_translate('en', ['es'], text = None, file=None)

    assert answer == [{'lang': 'es', 'text': 'Hola'}]


def test_cli_translate_NoLang(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "en")
    answer = cli_translate(None, ['es'], text = ["Hello"], file=None)

    assert answer == [{'lang': 'es', 'text': 'Hola'}]


def test_cli_translate_NoTarget(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "es fr")
    answer = cli_translate('en', None, text = ["Hello"], file=None)
    
    assert answer == [{'lang': 'es', 'text': 'Hola'},{'lang': 'fr', 'text': 'Bonjour'}]


def test_cli_translate_file():
    answer = cli_translate('en', ['es'], text = None, file="audio_files/sample1/english.wav")
    
    assert answer == [{'lang': 'es', 'text': 'uno dos tres'}]