# -*- coding: utf-8 -*-
import appJar as aj
from typing import Any, Text, Dict, Tuple, Callable, NewType
from toolz.curried import curry


@curry
def colorMode(app: aj.appjar.gui, button: Text)-> None:
    """
    Changes the color mode of the app. NOT CURRENTLY IMPLEMENTED

    Args:
        app (aj.appjar.gui): what app object to manipulate
        button (Text): which button to get

    """
    mode = app.getRadioButton(button)
    if mode == "Night":
        # app.setBg("#B71C1C")
        # app.setFg("#ECEFF1")
        pass
    elif mode == "Normal":
        # app.setBg("#37474F")
        # app.setFg("#ECEFF1")
        pass


def makeUI(*, size: Tuple[int, int]=(720, 480),
           fullscreen: bool=False) ->aj.appjar.gui:
    """
    Makes an object that represents the GUI.

    Args:
        size Tuple[int, int]: The size of the screen
        fullscreen (bool): Should the app start in fullscreen mode?

    Returns:
        app (aj.appjar.gui): The main app object.
    """
    """
    Main function that creates the UI, requires size or fulscreen to be passed as a keyword argument
    """
    try:
        assert size or fullscreen
    except AssertionError as Err:
        raise ValueError(Err + "\nGeometry needs to be set")
    if not fullscreen:
        app = aj.gui("ROBh.aT Network: Dome Controller",
                     f"{size[0]}x{size[1]}")
    else:
        app = aj.gui("ROBh.aT Network: Dome Controller", "fullscreen")
    # app.setBg("#37474F")
    # app.setFg("#ECEFF1")
    app.setFont(14, font="Open Sans")
    app.addLabel("title", "ROBh.aT Network: Dome Controller",
                 0, 0, colspan=3, rowspan=1)
    return app
