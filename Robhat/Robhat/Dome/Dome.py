from . import Control, UI, Macros
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
import os
import threading
import numpy as np
import serial
from toolz.curried import curry, get
import appJar as aj
import PyCmdMessenger as cmd


def motorStatusMonitor(app: aj.appjar.gui, Messenger: cmd.PyCmdMessenger.CmdMessenger)-> Callable:
    t = Control.sendCommand(Messenger, "Status")
    d = {t[1][0]:t[1][1], t[1][2]:t[1][3]}
    def inner():
        nonlocal d
        nonlocal app
        app.openTab("Main", "Control")
        app.openLabelFrame("Status")
        app.setLabel("motorStatus", f"Motor A: \t\t {get('A', d, '???')}\nMotor B: \t\t {get('B', d, '???')}")
    return inner


def demo(board: cmd.arduino.ArduinoBoard, Messenger: cmd.PyCmdMessenger.CmdMessenger,*rest, MotorDefaultTime=1000, fullscreen=False) -> None:
    """Demo"""

    app = UI.makeUI(size=(720,480))
    if fullscreen:
        app.setGeometry("fullscreen")
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
    print("making status panel")
    app.addLabel("motorStatus", "Motor A: \t\t ??? \nMotor B: \t\t ???", 0, 0)
    def offBoth()->None:
        Control.sendCommand(Messenger, "MotorOff", "A")
        Control.sendCommand(Messenger, "MotorOff", "B")
    app.addButton(
        "offBoth",
        lambda *a: offBoth(),
        3, 0, colspan=1, rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("A", 1, 0)
    print("making A")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onAF", lambda *a: Control.sendCommand(Messenger, "MotorOn", "A", "F", MotorDefaultTime), 0, 0)
    app.addButton("onAR", lambda *a: Control.sendCommand(Messenger, "MotorOn", "A", "R", MotorDefaultTime), 0, 1)
    app.addButton(
        "offA",
        lambda *a: Control.sendCommand(Messenger, "MotorOff", "A"),
        1, 0,colspan=2,rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("B",1,2)
    print("making B")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Control.sendCommand(Messenger, "MotorOn", "B", "F", MotorDefaultTime),0,0)
    app.addButton("onBR", lambda *a: Control.sendCommand(Messenger, "MotorOn", "B", "R", MotorDefaultTime),0,1)
    app.addButton(
        "offB",
        lambda *a: Control.sendCommand(Messenger, "MotorOff","B"),
        1, 0, colspan=2, rowspan=1)

    app.stopLabelFrame()
    app.stopTab()

    app.startTab("Macros")
    print("making Macros")
    app.stopTab()

    app.startTab("Settings")
    print("makign settings")
    app.startLabelFrame("Display",1,0)
    app.addRadioButton("colorMode","Normal")
    app.addRadioButton("colorMode", "Night")
    app.setRadioButton("colorMode", "Normal", callFunction=False)
    app.setRadioButtonChangeFunction("colorMode",UI.colorMode(app))
    app.stopLabelFrame()
    app.stopTab()
    app.stopTabbedFrame()
    app.registerEvent(motorStatusMonitor(app, Messenger))
    app.registerEvent(lambda: UI.colorMode(app, "colorMode"))

    app.go()
    print("app is alive")
