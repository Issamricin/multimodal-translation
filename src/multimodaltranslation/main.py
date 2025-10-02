import subprocess
import time
from argparse import ArgumentParser, RawTextHelpFormatter
from http.server import HTTPServer
from pathlib import Path

from multimodaltranslation.audio.translate import translate_audio
from multimodaltranslation.libretranslate_server import Libretranslate_Server
from multimodaltranslation.server import MyHandler
from multimodaltranslation.text.translate import send_text
from multimodaltranslation.version import __version__


def main() -> None:
    """
    Entry point for the multimodal translator cli.

    Parses the command line arguments:
        - If the -s Y was provided then the server will start.
        - Else it will performe a translation on the provided text or audio.

    Args: 
        None

    Returns:
        None
    """
    parser = ArgumentParser(
        description=(
            "Multimodal Translator\n"
            "=====================\n\n"
            "You can either:\n"
            "  • Start the server and send API calls to get translated text or audio.\n"
            "  • Use the CLI flags to translate text or audio directly.\n\n"
            "Available languages:\n"
            "  en - English\n"
            "  it - Italian\n"
            "  es - Spanish\n"
            "  fr - French\n"
            "  zh - Chinese\n"
        ),
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Multimodal Translator {__version__}"
    )

    # --- Server options ---
    server_group = parser.add_argument_group("Server options")
    server_group.add_argument(
        "-s",
        help="Start server? (Y/N) [default: N]",
        type=str,
        nargs="?",
        default="N",
        metavar="Y|N",
    )
    server_group.add_argument(
        "-ap",
        help="Application server port [default: 8000]",
        type=int,
        nargs="?",
        default=8000,
        metavar="APP_PORT",
    )
    server_group.add_argument(
        "-lp",
        help="Library server port [default: 5000]",
        type=int,
        nargs="?",
        default=5000,
        metavar="LIB_PORT",
    )

    # --- Translation options ---
    trans_group = parser.add_argument_group("Translation options")
    trans_group.add_argument(
        "-o",
        help="Original language (e.g. en, fr)",
        type=str,
        nargs="?",
        default=None,
        metavar="LANG",
    )
    trans_group.add_argument(
        "-t",
        help="Target languages (space-separated, e.g. es it zh)",
        type=str,
        nargs="+",
        default=None,
        metavar="LANGS",
    )

    # --- Input options (mutually exclusive) ---
    input_group = parser.add_argument_group("Input options")
    exclusive = input_group.add_mutually_exclusive_group()
    exclusive.add_argument(
        "-txt",
        help="Text to translate",
        type=str,
        nargs="+",
        default=None,
        metavar="TEXT",
    )
    exclusive.add_argument(
        "-f",
        help="Audio file to translate",
        type=Path,
        default=None,
        metavar="FILE",
    )

    args = parser.parse_args()

    if args.s == "Y":
        start_server(args.ap, args.lp)
    else:
        print(cli_translate(args.o, args.t, args.txt, args.f, args.lp))

def cli_translate(original:str, target:list, text:str, file:str, port:int =5000) -> list:
    """
    Translates the provided text or audio file given through the cli. 
    You can only provide one and the other would be None.

    Args:
        original (str): The language code of the original text (e.g. en, es)
        target (list): List of language codes to translate the text to.
        text (str): The text to translate.
        file (str): Path of the audio file (would be None when text provided).
        port (int): The port on which the translator library would run on. [Default: 5000]

    Returns:
        list: List of translated text with their targeted language.
    """

    process = subprocess.Popen(
        [ "libretranslate", "--port", f"{port}"],  # disable api keys so that libretranslate does not creats sessions for the api databases.
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(4)
    o = original
    t = target
    txt = text
    f = file

    if o is None:
        o = input("Enter the original language of the text: ")

    if t is None:
        inp = input("Enter the target languages seperated by space: ")
        t = inp.split(" ")

    if txt is not None:
        cont = " ".join(txt)
        translated = send_text(cont, o, t, port)
        process.kill()
        process.wait()
    elif file is not None:
        cont = f

        try:
            with open(cont,"rb") as r:
                cont_bytes = r.read()
        except FileNotFoundError:    
            process.kill()
            process.wait()
            return ["FileNotFoundError: Make sure you provide the correct path."]

        translated = translate_audio(cont_bytes, o, t, port)
        process.kill()
        process.wait()
    else:
        cont = input("Enter the text you want to translate: ")
        translated = send_text(cont, o, t, port)
        process.kill()
        process.wait()

    return translated

def start_server(port:int =8000, libport:int =5000) -> None:
    """
    Starts the server. The server to accept api calls.

    Args:
        port (int): The port to start the server on. [Default: 8000]
        libport (int): The port to start the translating library on. [Default: 5000]

    Returns:
        None    
    """
    # Start the LibreTranslate server
    print("starting server ... ")
    try:
        lib_server = Libretranslate_Server()
        lib_server.start_libretranslate_server(libport=libport)
    except Exception:
        lib_server.stop_libretranslate_server()
        return print([f"-{libport} Port might be taken!"])

    MyHandler.set_libport(libport)
    try:
        server = HTTPServer(("localhost", port), MyHandler)

    except OSError:
        return print("Error: Ports are in use. You can change the ports using the -lp and -ap flags. (-h for more help)")    

    try:
        print(f"server started on localhost port: {port}")
        server.serve_forever()

    except KeyboardInterrupt:  
        lib_server.stop_libretranslate_server()      
        return print("\nClosing server...")




if __name__ == "__main__":
    main()
