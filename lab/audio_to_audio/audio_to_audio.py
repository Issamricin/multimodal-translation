# copied from https://www.geeksforgeeks.org/python/create-a-real-time-voice-translator-using-python/
# with correction also
import asyncio
import os
from pathlib import Path

import optional
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound3 import playsound

FLAG = 0

# A tuple containing all the language and
# codes of the language will be detcted
dic = ('afrikaans', 'af', 'albanian', 'sq',
       'amharic', 'am', 'arabic', 'ar',
       'armenian', 'hy', 'azerbaijani', 'az',
       'basque', 'eu', 'belarusian', 'be',
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian',
       'bg', 'catalan', 'ca', 'cebuano',
       'ceb', 'chichewa', 'ny', 'chinese (simplified)',
       'zh-cn', 'chinese (traditional)',
       'zh-tw', 'corsican', 'co', 'croatian', 'hr',
       'czech', 'cs', 'danish', 'da', 'dutch',
       'nl', 'english', 'en', 'esperanto', 'eo',
       'estonian', 'et', 'filipino', 'tl', 'finnish',
       'fi', 'french', 'fr', 'frisian', 'fy', 'galician',
       'gl', 'georgian', 'ka', 'german',
       'de', 'greek', 'el', 'gujarati', 'gu',
       'haitian creole', 'ht', 'hausa', 'ha',
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
       'hi', 'hmong', 'hmn', 'hungarian',
       'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian',
       'id', 'irish', 'ga', 'italian',
       'it', 'japanese', 'ja', 'javanese', 'jw',
       'kannada', 'kn', 'kazakh', 'kk', 'khmer',
       'km', 'korean', 'ko', 'kurdish (kurmanji)',
       'ku', 'kyrgyz', 'ky', 'lao', 'lo',
       'latin', 'la', 'latvian', 'lv', 'lithuanian',
       'lt', 'luxembourgish', 'lb',
       'macedonian', 'mk', 'malagasy', 'mg', 'malay',
       'ms', 'malayalam', 'ml', 'maltese',
       'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian',
       'mn', 'myanmar (burmese)', 'my',
       'nepali', 'ne', 'norwegian', 'no', 'odia', 'or',
       'pashto', 'ps', 'persian', 'fa',
       'polish', 'pl', 'portuguese', 'pt', 'punjabi',
       'pa', 'romanian', 'ro', 'russian',
       'ru', 'samoan', 'sm', 'scots gaelic', 'gd',
       'serbian', 'sr', 'sesotho', 'st',
       'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si',
       'slovak', 'sk', 'slovenian', 'sl',
       'somali', 'so', 'spanish', 'es', 'sundanese',
       'su', 'swahili', 'sw', 'swedish',
       'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu',
       'te', 'thai', 'th', 'turkish',
       'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur',
       'ug', 'uzbek', 'uz',
       'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
       'yiddish', 'yi', 'yoruba',
       'yo', 'zulu', 'zu')


# Capture Voice
# takes command through microphone
def takecommand() -> optional[str]:
    """takes command through microphone"""
    recognizer = sr.Recognizer()
    AUDIO_FILE = str(Path(__file__).resolve().parents[3].joinpath("audio_files")) + \
                                os.path.sep + 'sample1' + os.path.sep + "english.wav"
    
    audio = sr.AudioData.from_file(AUDIO_FILE)

    try:
        print("Recognizing.....")
        que = recognizer.recognize_google(audio, language='en-in')
        print(f"The User said {que}\n")
    except Exception:
        print("say that again please.....")
        return "None"
    return que

# Input from user
# Make input to lowercase
query = takecommand()
while query == "None" :
    query = takecommand()


def destination_language() -> str:
    """Destination language..."""
    print("Enter the language in which you\
    want to convert : Ex. Hindi , English , etc.")
    print()

    # Input destination language in
    # which the user wants to translate
    #to_lang = takecommand()
    #while (to_lang == "None"):
    #    to_lang = takecommand()
    #to_lang = to_lang.lower()
    #return to_lang
    return "arabic"

TO_LANG = destination_language()

# Mapping it with the code
while TO_LANG not in dic:
    print("Language in which you are trying\
    to convert is currently not available ,\
    please input some other language")
    print()
    TO_LANG = destination_language()

TO_LANG = dic[dic.index(TO_LANG)+1]


async def translate_text(que:str, dest:str =TO_LANG) -> optional[str]:
    async with Translator() as translator:
        result = await  translator.translate(que, dest)
        return result


# invoking Translator
#translator = Translator()


# Translating from src to dest
text_to_translate = asyncio.run(translate_text(query=query, dest=TO_LANG))

text = text_to_translate.text

# Using Google-Text-to-Speech ie, gTTS() method
# to speak the translated text into the
# destination language which is stored in to_lang.
# Also, we have given 3rd argument as False because
# by default it speaks very slowly
speak = gTTS(text=text, lang=TO_LANG, slow=False) # noqa: N806 pylint: disable=invalid-name

# Using save() method to save the translated
# speech in capture_voice.mp3
speak.save("captured_voice.mp3")

# Using OS module to run the translated voice.
playsound('captured_voice.mp3')
os.remove('captured_voice.mp3')

# Printing Output
print(text)
