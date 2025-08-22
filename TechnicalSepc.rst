
THIS SECTION FOR ISO
=====================

| The product owner wants to be able to send a title with the source language and a target language list to be translated to
| The product owner wants to be able to send a title and body with the source language and a targe list to be translated to

| The result of translation above will return a list of TextTransModel ( see model package) with the "targets" param is None since the same
 class can be used for request response . it is the same for BodyTransModel


| In order to test, you need to innstall the libretranslate server and start it locally see
  https://docs.libretranslate.com/guides/installation/

| The API usage  https://docs.libretranslate.com/guides/api_usage/
| There is a package src/libretranslate/api.py which shows the usage to call http calls or rest calls

| You need to implement the validator so there is a file under src/conf/languages.json  . The support from to many needs to be validated and
| you need to response with a given error json object see model which explain the issue

| Step:

The call wil come as a json string object and you need to marshal it into the model. The enum class LANGUAGES is the one which protect and does validation

| In summary
 you will have two calls. One for  title translation  and the other for title and body but the "title and the body" are a composite of one   which is title translate

| You need to allow command line execution for a given payload ( start with title only trans and later implement title and body)

| You need to have test cases which covers exception ( network) and ValidationError and success translation

| The code cover need to be up to 90% so you need to show the coverage report. Use Tox to execute coverage reprot with test

| In your test you don't need to have a server (libretranslate server) up since you can mock the server and product the network error etc..

| finally, you need to run tox staff from the list to make sure things are correct before your push your changes to remote repo. See dmc-view *development* for tox list https://github.com/Issamricin/dmc-view/blob/master/docs/source/contents/development.rst




THIS SECTION FOR ALAN
=====================

RST File Checker:
-----------------

https://rsted.info.ucl.ac.be/


Factory Pattern:
----------------

| https://realpython.com/factory-method-python/

| https://www.geeksforgeeks.org/python/factory-method-python-design-patterns/

| speech regonition

Speed Regonition:
-----------------

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


