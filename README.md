# ROBh.aTnetwork
## Motor Dome Controller for Winona State University
### Nick Meyer and Carl Ferkinhoff 2017
The Robotic OBservatory by hardware.astronomy and Telescope Network, an open hardware project for robotizing
small observatories.
MIT Licensed!
Coming Soon:
  * Schematics
  * Boxes

To install this package:
    ```shell
    git clone https://github.com/HARDWAREdotASTRO/ROBh.aTnetwork.git ROBhaT
    cd ROBhat
    pip install -U -e ./Robhat
    ```

Example use case is given in `ExampleUseCases/run.py`


### Style Guide for Contributors:
#### Python:
* Follow PEP8
* Use Python 3.6
* Use PEP484 Type Hints for ALL functions
* All functions **must** have a docstring
* Use [Google Docstring](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) format
* Spacing: **Four Spaces**. Just use spaces.
* Variables and functions are named in `camelCase`
* Classes, Modules, etc. are named with `UpperCamelCase`
* Important constants should be in `CAPS_WITH_UNDERSCORES`
* Keyword-only arguments **must** be after `*rest`

#### Arduino:
* All files must be useable with both ArduinoIDE and PlatformIO
* Declare constants with `const`
* Declare constants before functions
* All timers should work in millisecond units
* Naming as in Python

#### User Interface:
* Use [Google's Material Color Palette](https://material.io/guidelines/style/color.html)
* Big buttons preferred (touch screens)
* Tabbed displays are preferable to scrolling displays

![Picture of Current UI](https://raw.githubusercontent.com/HARDWAREdotASTRO/ROBh.aTnetwork/master/temp_UI.PNG)
