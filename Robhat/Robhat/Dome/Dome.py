from . import Serial, UI
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
import os
import threading
import numpy as np
import serial
from toolz.curried import curry, get
import appjar as aj

def motorStatusMonitor(app: aj.appjar.gui, con: serial.Serial)-> Dict[Text,Text]:
    try:
        Serial.ensureConnected(con)
        t = {con.readline().decode("ascii").split(": \t\t ") for i in range(2)}
    except:
        t = {"A":"???","B":"???"}
    def inner():
        nonlocal t
        nonlocal app
        app.openTab("Main", "Control")
        app.openLabelFrame("Status")
        app.setLabel("motorStatus", f"Motor A: \t\t {get('A', t, '???')}\nMotor B: \t\t {get('B',t, '???')}")
    return inner


def demo(con: serial.Serial) -> None:
    """Demo"""

    app = UI.makeUI(size=(720,480))
    app.setSticky("nesw")
    app.setStretch("both")
    # app.setInPadding([25,25])
    # app.setPadding([20,20])

    app.startTabbedFrame("Main")
    app.startTab("Control")

    app.startLabelFrame("Status",1,1)
    app.setSticky("nesw")
    app.setStretch("both")
    # x = np.linspace(0, 1, 100)
    # y = np.sin(x)
    # axes = app.addPlot("plot1", x, y, 0,0, 2,1)
    app.addLabel("motorStatus", "Motor A: \t\t ??? \nMotor B: \t\t ???", 0, 0)

    app.addButton(
        "offBoth",
        lambda *a: Serial.sendCommand(con, message="offA&offB"),
        3, 0, colspan=1, rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("A", 1, 0)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onAF", lambda *a: Serial.sendCommand(con, message="onAF"), 0, 0)
    app.addButton("onAR", lambda *a: Serial.sendCommand(con, message="onAR"), 0, 1)
    app.addButton(
        "offA",
        lambda *a: Serial.sendCommand(con, message="offA"),
        1, 0,colspan=2,rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("B",1,2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Serial.sendCommand(con, message="onBF"),0,0)
    app.addButton("onBR", lambda *a: Serial.sendCommand(con, message="onBR"),0,1)
    app.addButton(
        "offB",
        lambda *a: Serial.sendCommand(con, message="offB"),
        1, 0, colspan=2, rowspan=1)

    app.stopLabelFrame()
    app.stopTab()

    app.startTab("Macros")
    app.startN
    app.stopTab()

    app.startTab("Settings")
    app.startLabelFrame("Display",1,0)
    app.addRadioButton("colorMode","Normal")
    app.addRadioButton("colorMode", "Night")
    app.setRadioButton("colorMode", "Normal", callFunction=False)
    app.setRadioButtonChangeFunction("colorMode",UI.colorMode(app))
    app.stopLabelFrame()
    app.stopTab()
    app.stopTabbedFrame()
    app.registerEvent(motorStatusMonitor(app, con))
    app.registerEvent(lambda: UI.colorMode(app, "colorMode"))

    app.go()
