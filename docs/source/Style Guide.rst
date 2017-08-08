=============================
Style Guides for Contributors
=============================

Python
^^^^^^

-  Follow PEP8
-  Use Python 3.6
-  Use PEP484 Type Hints for ALL functions
-  All functions **must** have a docstring
-  Use `Google Docstring`_ format
-  Spacing: **Four Spaces**. Just use spaces.
-  Variables and functions are named in ``camelCase``
-  Classes, Modules, etc. are named with ``UpperCamelCase``
-  Important constants should be in ``CAPS_WITH_UNDERSCORES``
-  Keyword-only arguments **must** be after ``*rest``

Arduino
^^^^^^^

-  All files must be useable with both ArduinoIDE and PlatformIO
-  Declare constants with ``const``
-  Declare constants before functions
-  All timers should work in millisecond units
-  Naming as in Python

User Interface
^^^^^^^^^^^^^^

-  Use `Google’s Material Color Palette`_
-  Big buttons preferred (touch screens)
-  Tabbed displays are preferable to scrolling displays


.. _Google Docstring: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
.. _Google’s Material Color Palette: https://material.io/guidelines/style/color.html

