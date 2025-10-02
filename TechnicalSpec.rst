PREREQUISITES
=============

You need to install tox to run the workflow tox task or env run task.

| **tox check list before you push to remote repo**

.. code-block:: shell

   python -m pip install tox
   tox -v -s false -e pin-deps
   tox -e type -v -s false
   tox -v -s false | tee test_output.log
   tox -e coverage --sitepackages -v -s false
   tox -e wheel-test -s false
   tox -e check -v -s false
   tox -e isort -vv -s false
   tox -e black -vv -s false
   tox -e ruff -vv -s false
   tox -e prospector -vv -s false

So before pushing to the remote repository run the above commands one by one and check for errors and fix them.
After all are correct with no errors then you push to the remote repo on github.

THIS SECTION FOR ISO
====================

One language Text To Many languages Text Translation:
-----------------------------------------------------

| Your backend library ( multimedia-translator) does not know anything about the rest . The library is rest agonistic ( does not have any clue)
  So somebody will call your library  with a payload called "TextTransModel"
  Your library  will have its own implementation to translate into different languages ( LlibreTranslate local server ) . You Library needs to make sure the language are supported ( your library needs to adhere to the LiberateTranslate languages supported since your library has no capability to do endless languages but rather follows the LilbreTranslate)
  Your library needs to validate the model (TextTransModel) to make sure it can do the job. If one of the selected languages (targets or source ) is not supported, you need to raise an exception to explain this . The caller ( the web application which uses your library) will handle the exception .
  If the validation is green, your library will communicate with the server ( it is your implementation hidden to me as a caller. I don't care about your internal implementation ) and return back a python model  see below correction for the model (TextModel)


| Update the spec to explain the above in your branch as usual . Let me know . You can push the json object down to my section since I need them later

.. code-block:: shell

  class  TextModel(): # generic text with language can be used for response
      def __init__(self, text:str, lang:LANGUAGES) -> None:
          self.__title = title
          self.__lang = lang



  class TextTransModel(TextModel): # this is the one your receive

      def __init__(self, text:str, lang:LANGUAGES, targets:list[LANGUAGES]) -> None:
          uper().__init__(title, lang) # common
          self.__targets = targets  #



Now for the body, it will be the split into two calls for the above (TextTransModel) since  body and title  can be one if you send them as one text with "|" seperator ( saving two calls into one call) and once you get back the translated "title|body" you can split them anb build the response back ( You do it later since you need to implement the above first and make end to end integration test ( inside the main of the class as we use to do )


| In order to test, you need to innstall the libretranslate server and start it locally see
  https://docs.libretranslate.com/guides/installation/

| The API usage  https://docs.libretranslate.com/guides/api_usage/
| There is a package src/libretranslate/api.py which shows the usage to call http calls or rest calls

| You need to implement the validator so there is a file under src/conf/languages.json  . The support from to many needs to be validated and
| you need to response with a given error json object see model which explain the issue

| You need to avoid using third party liberary if possible to make http call(rest call with json payload)  **use native if you can** https://docs.python.org/3/library/http.client.html
|

| Step:

  The call wil come as a json string object and you need to marshal it into the model. The enum class LANGUAGES is the one which protect and does validation
  Always work in virtual env. so when you put the project on edit mode, it will bring your the dependencies
  Nothing is perfect  so limitation will be imposed and we can revisit and improve later ( iterative or evolution approach)


| In summary
  you will have two calls. One for  title translation  and the other for title and body but the "title and the body" are a composite of one   which is title translate

| You need to allow command line execution for a given payload ( start with title only trans and later implement title and body)

| You need to have test cases which covers exception ( network) and ValidationError and success translation

| The code cover need to be up to 90% so you need to show the coverage report. Use Tox to execute coverage reprot with test

| In your test you don't need to have a server (libretranslate server) up since you can mock the server and product the network error etc..

| finally, you need to run tox staff from the list to make sure things are correct before your push your changes to remote repo. See dmc-view *development* for tox list https://github.com/Issamricin/dmc-         view/blob/master/docs/source/contents/development.rst

|
| Example of a json object request which will come from the rest call from the web application (End Usage)

.. code-block:: shell

   {
    "title": "Hi there",
    "body": "I am the body of the",
    "lang": "en",
    "targets": [
        "se",
        "pl"
    ]
   }


| Example of the response  which sent back to web view

.. code-block:: shell

  [
    {
        "title": "Hej där",
        "body": "Jag är kroppend av meddelande",
        "lang": "se"
    },
    {
        "title": "blalaaa",
        "body": "polizika blah",
        "lang": "pl"
    }
  ]



One Audio language to Many languages Text Translation:
------------------------------------------------------

| See the src/multimedia_translator/audio_to_text which we are working on  https://github.com/cmusphinx/pocketsphinx which is being wrapped by speech_recognition
  Google API is good but it has limitation and you can check that
  In the model we have BytesIO but try to start with simple file and change the model signature if needed.
  The reason for BytesIO usage since the call will come from the web client with payload of stream which will will take it late (me)




One Audio language  to Many languages Audios Translation:
---------------------------------------------------------

| See the src/multimedia_translator/audio_to_audio  which uses googletrans and google api for text to speech we can look at the limitation and try to find another
  one source one as we did with text to text


Audio Search for a given language words(optional):
--------------------------------------------------

| We need to be able to search audio file for a given word in a given language
  for example, if I have an audio in Swedish and I want to search for a words such  as "eat", "bread"  in English; so I convert to
  the audio to English and do the search for the given English words.
  This is optional now and it is part of pocketsphinx see https://cmusphinx.github.io/wiki/tutorialpocketsphinx/#advanced-usage
  It also allow us to build a language model which we will not do now but who knows


Audio:
------

 Currently, SpeechRecognition supports the following file formats:

 WAV: must be in PCM/LPCM format ( we support this only)
 AIFF AIFF-C
 FLAC: must be native FLAC format; OGG-FLAC is not supported


| Though a WAV file can contain compressed audio, the most common WAV audio format is uncompressed audio in the linear pulse-code modulation (LPCM) format.
   LPCM is also the standard audio coding format for audio CDs, which store two-channel LPCM audio sampled at 44.1 kHz with 16 bits per sample.

| online play
  https://www.luxa.org/audio


No Noise filter implemtation. No suppport for  ambient noise   . the file needs to be clean of noise. This can be implemented in the future as TODO or techincal debt as per scipy digital signal processing
see https://realpython.com/python-scipy-cluster-optimize/
see chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://greenteapress.com/thinkdsp/thinkdsp.pdf

Speed Recognition:
------------------

| https://realpython.com/python-speech-recognition/

| https://www.geeksforgeeks.org/python/create-a-real-time-voice-translator-using-python/


Video Translation:
------------------

| A list
 https://github.com/topics/video-translation

| Video to Audio convert using Python
 https://www.geeksforgeeks.org/python/video-to-audio-convert-using-python/


| Video Translator ( subtitle trans)
 A Python-based web application that extracts video subtitles and translates them to English using the OpenAI Whisper library.
 https://github.com/andreypudov/video-translator

| translate video to any language translate a video to any language using Python, Wav2Lip and Google Wavenet
  https://www.reddit.com/r/Python/comments/k6se53/translate_a_video_to_any_language_using_python/

| Creating a Speech Translator with Python (YouTube)
 https://www.youtube.com/watch?v=rRR4eVr9j1k


| Translate a video to any language using Python, Wav2Lip and Google Wavenet
 https://www.reddit.com/r/Python/comments/k6se53/translate_a_video_to_any_language_using_python/



| Developing Video translation
 https://medium.com/@jianchang512/developing-a-video-translation-and-dubbing-tool-using-python-a1120b8b5b47
 https://dev.to/devasservice/video-captioning-and-translating-with-python-and-streamlit-5e0k

| 

THIS SECTION FOR REWAN
======================

Read the prerequisites at the top of this file (tox), understand the commands.
And make sure to never push to the remote repo before doing the prerequisites part.

Testing the code in the src folder:
-----------------------------------

Install pytest and coverage in your env.
This is the documentation for the coverage: https://coverage.readthedocs.io/en/7.7.0/

The tests should cover about 95% of the code.
To check how much your tests are covering:
$ coverage run -m pytest
$ coverage report -m



|

THIS SECTION FOR ALAN
=====================

Moved from iso part:
--------------------

| The product owner wants to be able to send a title with the source language and a target language list to be translated to
| The product owner wants to be able to send a title and body with the source language and a targe list to be translated to

| The result of translation above will return a list of TextTransModel ( see model package) with the "targets" param is None since the same
 class can be used for request response . it is the same for BodyTransModel


RST File Checker:
-----------------

https://rsted.info.ucl.ac.be/


Factory Pattern:
----------------
| https://realpython.com/python-type-hints-multiple-types/#annotate-the-return-value-of-a-factory-function

| https://realpython.com/factory-method-python/

| https://www.geeksforgeeks.org/python/factory-method-python-design-patterns/


