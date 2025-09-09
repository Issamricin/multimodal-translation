audio to text observation
=========================

=================
speech recognizer
=================

------
sphinx
------

Using the sphinx recognizer from speach recognizer has limitations, You can only lisen to english audio. You can train the model i think but thats complicated.


-----------
google-free
-----------

Its unreliable for other languages. It sends a forbidden 403 error. Also only works for english.


----
vosk
----

official documentation: https://alphacephei.com/vosk/
github repository: https://github.com/alphacep/vosk-api

To use this lib, first you need to install it using pip: pip install vosk

You need to import the wave lib. which is python native library and you don't need to install it since its built in.
You need it since the vosk needs raw pcm audio, and we use wave to read the .wav file into raw data.

vosk only accepts wav thus i used ffmpeg command to convert other types to wav. And we can't add this ffmpeg into python dependencies thus it must
be installed seperately as its a system-level dependency. "sudo apt install ffmpeg"