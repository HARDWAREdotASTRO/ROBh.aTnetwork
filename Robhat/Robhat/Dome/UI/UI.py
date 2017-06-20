import appJar as aj
from typing import Any, Text, Dict, Sequence, List, Tuple, Callable, Union, NewType
from toolz.curried import pipe, get, map, filter, reduce, operator as op, assoc

ButtonType = NewType('ButtonType', Tuple[Text, Callable[[], Any]])

global BUTTONS
BUTTONS = dict() #type: Dict[Text, ButtonType]


def makeUI(*, size: Tuple = (720,480)) -> aj.appjar.gui :
    """
    Main function that creates the UI, requires size to be passed as a keyword argument
    """
    global BUTTONS
    app = aj.gui("ROBh.aT Network: Dome Controller", f"{size[0]}x{size[1]}")
    # app.setBg("#37474F")
    # app.setFg("#ECEFF1")
    app.setFont(12, font="Open Sans")
    app.addLabel("title", "ROBh.aT Network: Dome Controller", 0, 0, 3)
    return app
