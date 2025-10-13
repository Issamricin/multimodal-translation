import sys
import warnings
from unittest.mock import MagicMock, patch

from multimodaltranslation.main import (
    cli_translate,
    install_language,
    main,
    start_server,
)


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


def test_install_language_success():
    """Should call package.install_from_path and print success message."""
    path = "/fake/path/model.zip"

    with patch("multimodaltranslation.main.package.install_from_path") as mock_install, \
         patch("builtins.print") as mock_print:
        install_language(path)

    mock_install.assert_called_once_with(path)
    mock_print.assert_any_call("Installing language ...")


def test_install_language_invalid_model():
    """Should catch exception and print an error message."""
    path = "/fake/path/invalid.zip"

    with patch("multimodaltranslation.main.package.install_from_path", side_effect=Exception("bad zip")), \
         patch("builtins.print") as mock_print:
        install_language(path)

    # The package.install_from_path should be called once
    mock_print.assert_any_call("Installing language ...")
    mock_print.assert_any_call(
        "Error: Not a valid argos model (must be zip archive)\n"
        "Visit https://www.argosopentech.com/argospm/index/ to install models"
    )


def test_start_server_normal():
    """Server starts normally and calls serve_forever."""
    with patch("multimodaltranslation.main.HTTPServer") as mock_http, \
         patch("builtins.print") as mock_print:
        mock_server = MagicMock()
        mock_http.return_value = mock_server

        start_server(8000)

    # It should print startup messages
    mock_print.assert_any_call("starting server ... ")
    mock_print.assert_any_call("Server started on localhost port: 8000")

    # It should create the server and call serve_forever
    mock_http.assert_called_once_with(("localhost", 8000), mock_http.call_args[0][1])
    mock_server.serve_forever.assert_called_once()


def test_start_server_oserror():
    """If port is already in use, prints an error message and returns."""
    with patch("multimodaltranslation.main.HTTPServer", side_effect=OSError), \
         patch("builtins.print") as mock_print:
        start_server(8000)

    mock_print.assert_any_call("starting server ... ")
    mock_print.assert_any_call(
        "Error: Ports are in use. You can change the ports using the -ap flag. (-h for more help)"
    )


def test_start_server_keyboard_interrupt():
    """If KeyboardInterrupt occurs during serve_forever, prints closing message."""
    with patch("multimodaltranslation.main.HTTPServer") as mock_http, \
         patch("builtins.print") as mock_print:
        mock_server = MagicMock()
        mock_http.return_value = mock_server
        mock_server.serve_forever.side_effect = KeyboardInterrupt

        start_server(8000)

    mock_print.assert_any_call("starting server ... ")
    mock_print.assert_any_call("Server started on localhost port: 8000")
    mock_print.assert_any_call("\nClosing server...")
