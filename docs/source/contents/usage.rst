Usage
=====

------------
Installation
------------

| **multimodal-translation** is available on PyPI hence you can use `pip` to install it.

It is recommended to perform the installation in an isolated `python virtual environment` (env).
You can create and activate an `env` using any tool of your preference (ie `virtualenv`, `venv`, `pyenv`).

Assuming you have 'activated' a `python virtual environment`:

.. code-block:: shell

  python -m pip install multimodal-translation


---------------
Simple Use Case
---------------

To use the application through the cli:

If you want to translate a text:

.. code-block:: shell

  translator -o en -t fr es -txt Hello

| **o**: Original language of the text you want to translate.
| **t**: Target language you want the text to be translated to.
| **txt**: The text you want to translate.

If you want to translate an audio file:

.. code-block:: shell

  cd audio_files/sample1
  translator -o en -t fr es -f english.wav

| **o**: Original language of the audio file you want to translate.
| **t**: Target language you want the audio file to be translated to.
| **f**: The audio file you want to translate.

Or you can directly provide the full path like so:

.. code-block:: shell

  translator -o zh -t fr es -f audio_files/sample1/chinese.flac

Moreover, you can also run a live server. Send the api requests to the server and get the responses back as a json.

.. code-block:: shell

  translator -s Y

Then in your python code:

To translate some text use the /text route:

.. code-block:: python

    my_object = {"text": "Hello", "lang": "en", "targets": ["it","es"]}
    url = "http://localhost:8000/text"

    response = requests.post(url, json=my_object, headers={"Content-Type": "application/json"})
    print(response.json())

To translate an audio file use the /audio route:

.. code-block:: python

    url = "http://localhost:8000/audio"

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()    

    audio_str = audio_bytes.hex()
    files = {
        "audio": audio_str,
        "lang":"en",
        "targets": ["fr","es"]  
    }

    response = requests.post(url, json=files)
    print(response.text)

Note: Make sure you convert the audio file to bytes and then **encode them using .hex()** before sending them.

Then response will come as following:

.. code-block:: shell

    [{'text': 'bonjour', 'lang': 'fr'}, {'text': '哈啰', 'lang': 'zh'}]

  
Available languages for now:

- en "english"
- fr "french"
- it "italian"
- es "spanish"
- zh "chinese"

The ports that the library runs on by default might be in use. 
That's why there are flags for this library and for the translating library to change the ports on which the servers run on.

.. code-block:: shell

    translator -s Y -lp 4000 -ap 5000
  

-lp flag is for the translating library port.
-ap flag is for the application port.
  
--------------
Running PyTest
--------------
| PyTest can be run from command line.

.. code-block:: shell

  python -m pip install -e . multimodal-translation
  pytest



