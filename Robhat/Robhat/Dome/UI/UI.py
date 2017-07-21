import appJar as aj
from typing import Any, Text, Dict, Tuple, Callable, NewType
from toolz.curried import curry

ButtonType = NewType('ButtonType', Tuple[Text, Callable[[], Any]])

global BUTTONS
BUTTONS = dict()  # type: Dict[Text, ButtonType]


@curry
def colorMode(app: aj.appjar.gui, button: Text )-> None:
    mode = app.getRadioButton(button)
    if mode == "Night":
        # app.setBg("#B71C1C")
        # app.setFg("#ECEFF1")
        pass
    elif mode == "Normal":
        # app.setBg("#37474F")
        # app.setFg("#ECEFF1")
        pass


def makeUI(*, size: Tuple = (720,480), fullscreen: bool = False) -> aj.appjar.gui:
    """
    Main function that creates the UI, requires size or fulscreen to be passed as a keyword argument
    """
    global BUTTONS
    try:
        assert size or fullscreen
    except AssertionError as Err:
        raise ValueError(Err + "\nGeometry needs to be set")
    if not fullscreen:
        app = aj.gui("ROBh.aT Network: Dome Controller", f"{size[0]}x{size[1]}")
    else:
        app = aj.gui("ROBh.aT Network: Dome Controller", "fullscreen")
    # app.setBg("#37474F")
    # app.setFg("#ECEFF1")
    app.setFont(14, font="Open Sans")
    app.addLabel("title", "ROBh.aT Network: Dome Controller", 0, 0, colspan=3, rowspan=1)
    return app
