'''
Package for **Text Translation**

You send the text you want to translate, along side the original language of the text;\n
and the targets languages you want to translate to.

This module will then translate the text into the desired languages.

example:
    >>> responses = translate_text(text, lang, targets)
    >>> print(responses)
    >>> [{"text": "un deux trois", "lang": "fr"}, {"text": "one two three", "lang": "en"}]

'''
