| |build| |release_version| |wheel| 
| |docs| |pylint| |supported_versions|
| |ruff| |gh-lic| |commits_since_specific_tag_on_main|

|logo|

|translator_gif|
|translator_gif_2|


What is multimodal translation?
-------------------------------

| Multimodal translation is an advanced form of communication and translation that integrates and interprets information
  from various sources, such as text, images, audio, and video, to convey a message accurately.

  Simply put, it's translating content across various types of media.

Why is multimodality important?
-------------------------------

|  When translating information that is in different formats and media types, it's hard to effectively grasp the context,
|  and truly understand the meaning behind them. 
|
|  That's where multimodal translation comes in handy. It helps in understanding the context correctly and translate them accurately
|  by using multiple modals like text, audio, video, etc... This technology is very important in systems where context awareness is required.
|
Types of multimodal translation:
--------------------------------

- **Text-to-text:** This is the simplest form where you can translate text from one language to another language.
- **Audio-to-text:** Here the audio is transcribed and then translated also into several languages.
- **Audio-to-audio:** May be implemented in the future. It's the same concept as audio to text but the output remains in audio format.

Technology used:
----------------

- **Speech recognition:** Important to recognize spoken language for interpretation and translation. Output can then be in text or audio format.


Limitations:
------------

- **language support:** Hard to support all languages, since every language has its own modal that has to be trained and installed into the application.
- **Maintaining context:** The context may change across different media. So it's a must to ensure the context remains correct.


Improvements:
-------------

* As mentioned above, audio to audio will be implemented in the future. Other media types can also be implemented like videos and images.

References:
-----------

* `The Era of Multimodal Translation <https://www.kantanai.io/localization-now-the-era-of-multimodal-translation/>`_
* `What is Multimodal Translation <https://www.educative.io/answers/what-is-multimodal-translation>`_


.. |build| image:: https://github.com/alanmehio/multimodal-translation/actions/workflows/ci_cd.yaml/badge.svg
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/alanmehio/multimodal-translation/actions/


.. Documentation

.. |docs| image:: https://img.shields.io/readthedocs/multimodal-translation/latest?logo=readthedocs&logoColor=lightblue
    :alt: Read the Docs (version)
    :target: https://dmc-view.readthedocs.io/en/latest/

.. |pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint

.. PyPI

.. |release_version| image:: https://img.shields.io/pypi/v/multimodal-translation
    :alt: Production Version
    :target: https://pypi.org/project/multimodal-translation

.. |wheel| image:: https://img.shields.io/pypi/wheel/multimodal-translation?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/multimodal-translation

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/multimodal-translation?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/multimodal-translation

.. Github Releases & Tags

.. |commits_since_specific_tag_on_main| image:: https://img.shields.io/github/commits-since/alanmehio/multimodal-translation/v0.0.1/main?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/alanmehio/multimodal-translation/compare/v0.0.1..main

.. LICENSE (eg AGPL, MIT)
.. Github License

.. |gh-lic| image:: https://img.shields.io/badge/license-GNU_Affero-orange
    :alt: GitHub
    :target: https://github.com/alanmehio/multimodal-translation/blob/main/LICENSE


.. Ruff linter for Fast Python Linting

.. |ruff| image:: https://img.shields.io/badge/codestyle-ruff-000000.svg
    :alt: Ruff
    :target: https://docs.astral.sh/ruff/


.. |logo| image:: media/muiltimodal-translation-small.jpg
                :alt: multimodal translator

.. |translator_gif| image:: media/translator.gif
   :alt: Demo Preview
   :width: 800
   :height: 300

.. |translator_gif_2| image:: media/translator_audio.gif
   :alt: Demo Preview
   :width: 800
   :height: 280