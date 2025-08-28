In order to run the one to many api, you have to do the following:

1- you need to have the libretranslate server live and running:
    - Install libretranslate using pip: pip install libretranslate.
    - Open a terminal.
    - Run the server: libretranslate.
    - You need to install the langaues you want in your local server (check lab/text/installing_langModels.py).

2- You need to run the flask server application:
    - Run the one_to_many.py script in a different terminal.
    - 

3- You can test as a client:
    - Run the sender_dummy.py to check how the data is received by the flask app.
    - Try to put a lang that is not supported, you will get a json explaining the error.


Note: 
    - In total you will need three terminal to test this locally.
    - Also when you install libretranslate only french and english are available. 
    So install the langauges needed and edit the langauge list in the server to contain only the installed langauge models so it doesn't crash.