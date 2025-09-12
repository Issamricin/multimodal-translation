'''
Package for **Audio Translation**

You send the bytes of the audio file you have, along side the language of the audio, and the targets languages you want to translate to.
This module will then convert the file to wav form, get the transcription of the audio, and finally translate it to the desired target languages.

example:
    >>> responses = translate_audio(audio_bytes,  lang, targets)
    >>> print(responses)
    >>> [{"text": "un deux trois", "lang": "fr"}, {"text": "one two three", "lang": "en"}]

'''
