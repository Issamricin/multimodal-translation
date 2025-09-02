Development
===========

| Insall `pip`

.. code-block:: shell

    python3 -m pip install


| Clone the repository

.. code-block:: shell

    git clone git@github.com:alanmehio/multimodal-translator.git
    cd  multimodal-translator

| Make the project in edit mode

.. code-block:: shell

    pip install -e .

Then, for any changes in the code you can execute it from command line

.. code-block:: shell

   multimodal-translation



Development Notes
~~~~~~~~~~~~~~~~~
Testing, Documentation Building, Scripts, CI/CD, Static Code Analysis for this project.

1. **Test Suite**, using `pytest`_, located in `tests` dir
2. **Parallel Execution** of Unit Tests, on multiple cpu's
3. **Documentation Pages**, hosted on `readthedocs` server, located in `docs` dir
4. **CI(Continuous Integration)/CD(Continuous Delivery) Pipeline**, running on `Github Actions`, defined in `.github/`

   a. **Test Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platforms: `ubuntu-latest`
      2. Python Interpreters:  `3.13`
   b. **Continuous Deployment**

      `Production`

         1. **Python Distristribution** to `pypi.org`_, on `tags` **v***, pushed to `main` branch
         2. **Docker Image** to `Dockerhub`_, on every push, with automatic `Image Tagging`

      `Staging`

         3. **Python Distristribution** to `test.pypi.org`_, on "pre-release" `tags` **v*-rc**, pushed to `release` branch

   c. **Configurable Policies** for `Docker`, and `Static Code Analysis` Workflows
5. **Automation**, using `tox`_, driven by single `tox.ini` file

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build`_ python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org`_ and `test.pypi.org`_ servers
   d. **Type Check Command**, using `mypy`_
   e. **Lint** *Check* and `Apply` commands, using the fast `Ruff`_ linter, along with `isort`_ and `black`_


Prerequisites
-------------

You need to have `Python` installed for Development

API Documentation
-----------------
We follow Google style documentation for packages, modules, classes, methods

.. LINKS

| `Tox <https://tox.wiki/en/latest/>`__

| `Pytest <https://docs.pytest.org/en/7.1.x/>`__

| `Build <https://github.com/pypa/build>`__

| `Docker <https://hub.docker.com/>`__

| `pypi.org <https://pypi.org/>`__

| `test.pypi.org <https://test.pypi.org/>`__

| `mypy <https://mypy.readthedocs.io/en/stable/>`__

| `Ruff <https://docs.astral.sh/ruff/>`__

| `Isort <https://pycqa.github.io/isort/>`__

| `Black <https://black.readthedocs.io/en/stable/>`__

| `Google API docs <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`__

