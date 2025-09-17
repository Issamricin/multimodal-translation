from multimodaltranslation.version import __version__
from argparse import ArgumentParser
from multimodaltranslation.server import MyHandler
from multimodaltranslation.text.translate import translate_text
from multimodaltranslation.audio.translate import translate_audio
from http.server import HTTPServer

import subprocess
import time
from pathlib import Path

def main() -> None:
    port = 8000

    LANGUAGE = [
     "en",
     "it",
     "es",
     "fr",
     "zh"
    ]

    parser = ArgumentParser(
        description= f"You can either start the server and send api calls to get the translated text or audio back. \
        Otherwise you can use the cli flags to translate direclty. Available languages are {LANGUAGE} for english, italian, spanish, french, and chinese respectively"
    )

    parser.add_argument("--version", action="version", version=f"Multimodal Translator {__version__}")

    parser.add_argument(
        "-s",
        help='Start server Y/N ?',
        type=str,
        nargs="?",
        default="N",
        metavar="server",
    )
    parser.add_argument(
        "-o",
        help='original language of the text or audio',
        type=str,
        nargs="?",
        default=None,
        metavar="original lanuage",
    )
    parser.add_argument(
        "-t",
        help='target lanuages you want to translate to',
        type=str,
        nargs="+",
        default=None,
        metavar="target",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-txt",
        help='text you want to translate',
        type=str,
        nargs="+",
        default=None,
        metavar="text",
    )
    group.add_argument(
        '-f',
        help='audio file you want to translate',
        type=Path,
        default=None,
        metavar="audio file",
    )

    args = parser.parse_args()

    if args.s == "Y":
        start_server(port)
    else:
        cli_translate(args.o, args.t, args.txt, args.f)
    
def cli_translate(original, target, text, file):

    process = subprocess.Popen(
        [ "libretranslate", "--port", "5000"],  # adjust port if needed
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    o = original
    t = target
    txt = text
    f = file

    if o == None:
        o = input("Enter the original language of the text: ")

    if t == None:
        t = input("Enter the target languages seperated by space: ")
        t = t.split(" ")

    if txt != None:
        cont = " ".join(txt)
        translated = translate_text(cont, o, t)
    elif file != None:
        cont = f

        try:
            with open(cont,"rb") as r:
                cont_bytes = r.read()
        except FileNotFoundError:    
            process.kill()
            process.wait()
            return print("FileNotFoundError: Make sure you provide the correct path.")

        translated = translate_audio(cont_bytes, o, t)
    else:
        cont = input("Enter the text you want to translate: ")
        translated = translate_text(cont, o, t)

    print(translated)

def start_server(port):
    # Start the LibreTranslate server
    print("starting server ... ")
    process = subprocess.Popen(
        [ "libretranslate", "--port", "5000"],  # adjust port if needed
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(4) 

    server = HTTPServer(("localhost", port), MyHandler)
    print(f"server started on localhost port: {port}")
    try:
        server.serve_forever()

    except KeyboardInterrupt:        
        print("\nClosing server...")
        process.kill()
        process.wait()




if __name__ == "__main__":  # this is important so that it does not run from pytest
    main()