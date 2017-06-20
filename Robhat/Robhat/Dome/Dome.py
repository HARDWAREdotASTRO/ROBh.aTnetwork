from . import Serial, UI
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
import os
import threading
import numpy as np

def demo() -> None:
    """Demo"""

    app = UI.makeUI(size=(720,480))
    app.setSticky("nesw")
    app.setStretch("both")
    # app.setInPadding([25,25])
    # app.setPadding([20,20])

    app.startLabelFrame("Status",1,1)
    app.setSticky("nesw")
    app.setStretch("both")
    x = np.linspace(0, 1, 100)
    y = np.sin(x)
    # axes = app.addPlot("plot1", x, y, 0,0, 2,1)
    app.addButton(
        "offBoth",
        lambda *a: Serial.sendCommand(con, message="offA&offB"),
        999, 0, 999, 1)
    app.stopLabelFrame()

    app.startLabelFrame("A", 1, 0)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onAF", lambda *a: Serial.sendCommand(con, message="onAF"), 0, 0)
    app.addButton("onAR", lambda *a: Serial.sendCommand(con, message="onAR"), 0, 1)
    # app.addButtons(
    #     ["onAF", "onAR"],
    #     [lambda *a: Serial.sendCommand(con, message="onAF"),
    #     lambda *a: Serial.sendCommand(con, message="onAR")],
    #     0, 0, 2, 1)

    app.addButton(
        "offA",
        lambda *a: Serial.sendCommand(con, message="offA"),
        1, 0,2,1)
    app.stopLabelFrame()

    app.startLabelFrame("B",1,2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Serial.sendCommand(con, message="onBF"),0,0)
    app.addButton("onBR", lambda *a: Serial.sendCommand(con, message="onBR"),0,1)
    # app.addButtons(
    #     ["onBF", "onBR"],
    #     [lambda *a: Serial.sendCommand(con, message="onBF"),
    #     lambda *a: Serial.sendCommand(con, message="onBR")],
    #     0,0,2,1)

    app.addButton(
        "offB",
        lambda *a: Serial.sendCommand(con, message="offB"),
        1, 0, 2, 1)

    app.stopLabelFrame()
    app.go()
