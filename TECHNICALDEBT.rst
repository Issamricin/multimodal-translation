Technical Debt
==============
| The list below represent our technical debt which we will be addressed in the coming future
| We will check the debt which is done by a |done| 
 

Mocking the test case server:
-----------------------------

| In your test you don't need to have a server up since you can mock the server and product the network error etc..
| Currently it is starting a server, doing tests, and then closing the server.


New Features:
-------------

1- Audio to many Audios translations
2- Video to many many text translations ( pure text)
3- Video to man Video translations
4- Video to text translated on the videos


Audio Search for a given language words(optional):
--------------------------------------------------

| We need to be able to search audio file for a given word in a given language
  for example, if I have an audio in Swedish and I want to search for a words such  as "eat", "bread"  in English; so I convert to
  the audio to English and do the search for the given English words.
  This is optional now and it is part of pocketsphinx see https://cmusphinx.github.io/wiki/tutorialpocketsphinx/#advanced-usage
  It also allow us to build a language model which we will not do now but who knows


| Format limitation
 Currently, SpeechRecognition supports the following file formats:

 WAV: must be in PCM/LPCM format ( we support this only)
 AIFF AIFF-C
 FLAC: must be native FLAC format; OGG-FLAC is not supported


| Though a WAV file can contain compressed audio, the most common WAV audio format is uncompressed audio in the linear pulse-code modulation (LPCM) format.
   LPCM is also the standard audio coding format for audio CDs, which store two-channel LPCM audio sampled at 44.1 kHz with 16 bits per sample.

| online play
  https://www.luxa.org/audio


| No Noise filter implemtation. No suppport for  ambient noise   . the file needs to be clean of noise. This can be implemented in the future as TODO or techincal debt as per scipy digital signal processing
 see https://realpython.com/python-scipy-cluster-optimize/
 see chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://greenteapress.com/thinkdsp/thinkdsp.pdf




.. |done| image::  https://img.shields.io/badge/DONE-green
            :alt: DONE
