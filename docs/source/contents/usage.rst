Usage
=====

------------
Installation
------------

| **rfcentralral** is available on PyPI hence you can use `pip` to install it.

It is recommended to perform the installation in an isolated `python virtual environment` (env).
You can create and activate an `env` using any tool of your preference (ie `virtualenv`, `venv`, `pyenv`).

Assuming you have 'activated' a `python virtual environment`:

.. code-block:: shell

  python -m pip install rfcentral


---------------
Simple Use Case
---------------

.. code-block:: shell

  rfcentral -p 65.55 -d ttyACM0

| **p**  power threshold to sent alarm to the RF server
| **d**: RF receiver device port name




--------------
Running PyTest
--------------
| PyTest can be run from command line.

.. code-block:: shell

  python -m pip install -e . rfcentral[test]
  pytest



