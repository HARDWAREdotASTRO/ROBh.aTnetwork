from . import Control, UI, Macros
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
import os
import threading
from toolz.curried import curry, get
import appJar as aj
from math import ceil
import PyCmdMessenger as cmd
import configparser
import asyncio as aio



def readConfig(configFile: Text = "./.config") -> Dict[Text, Any]:
    """
    Reads a configuration file.
    """
    config = configparser.ConfigParser()
    config.read(configFile)
    settings = dict()
    settings["SerialPort"] = config["DEFAULT"]["SerialPort"]
    settings["PollTime"] = int(config["DEFAULT"]["PollTime"])
    settings["BaudRate"] = int(config["DEFAULT"]["BaudRate"])
    return settings


def motorStatusMonitor(app: aj.appjar.gui, Messenger: cmd.PyCmdMessenger.CmdMessenger)-> Callable:
    def getStatus():
        nonlocal Messenger
        nonlocal app
        # Ask for the current status of the motor
        t = Control.sendCommand(Messenger, "Status")
        d = {t[1][0]: t[1][1], t[1][2]: t[1][3]}  # parse the response
        def statusChanger():  # need a closure to write to the app when called
            nonlocal d  # use the message from above
            nonlocal app  # use the app passed with motorStatusMonitor
            app.openTab("Main", "Control")
            app.openLabelFrame("Status")
            app.setLabel("motorStatus", f"Motor A: \t\t {get('A', d, '???')}\nMotor B: \t\t {get('B', d, '???')}") # Print the status of the motors to the app
        return statusChanger

    return getStatus()



def demo(board: cmd.arduino.ArduinoBoard, Messenger: cmd.PyCmdMessenger.CmdMessenger, *rest, MotorDefaultTime=1000, fullscreen=False) -> None:
    """Demo"""

    app = UI.makeUI(size=(720, 480))
    app.setPollTime(ceil(MotorDefaultTime/1000)) #AppJar uses seconds as its time, so divide by 1000 and get the ceil of it (longer poll times preferred to shorter ones.)
    if fullscreen:
        app.setGeometry("fullscreen")
    app.setSticky("nesw")
    app.setStretch("both")
    # app.setInPadding([25,25])
    # app.setPadding([20,20])

    app.startTabbedFrame("Main")
    app.startTab("Control")

    app.startLabelFrame("Status", 1, 1)
    app.setSticky("nesw")
    app.setStretch("both")
    print("making status panel")
    app.addLabel("motorStatus", "Motor A: \t\t ??? \nMotor B: \t\t ???", 0, 0)

    def offBoth() -> None: # define a local function to turn off both motors
        _0 = Control.sendCommand(Messenger, "MotorOff", "A")
        del _0
        _1 = Control.sendCommand(Messenger, "MotorOff", "B")
        del _1

    app.addButton( # make me a button that turns off the motors!
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
    app.addButton("offA",
                        lambda *a: Control.sendCommand(Messenger, "MotorOff", "A"),
                        1, 0, colspan=2, rowspan=1)

    app.stopLabelFrame()

    app.startLabelFrame("B", 1, 2)
    print("making B")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Control.sendCommand(Messenger, "MotorOn", "B", "F", MotorDefaultTime), 0, 0)
    app.addButton("onBR", lambda *a: Control.sendCommand(Messenger, "MotorOn", "B", "R", MotorDefaultTime), 0, 1)
    app.addButton("offB",
                        lambda *a: Control.sendCommand(Messenger, "MotorOff", "B"),
                        1, 0, colspan=2, rowspan=1)

    app.stopLabelFrame()
    app.stopTab()

    app.startTab("Macros")
    print("making Macros")
    app.stopTab()

    app.startTab("Settings")
    print("making settings")
    app.startLabelFrame("Display", 1, 0)
    app.addRadioButton("colorMode", "Normal")
    app.addRadioButton("colorMode", "Night")
    app.setRadioButton("colorMode", "Normal", callFunction=False)
    app.setRadioButtonChangeFunction("colorMode", UI.colorMode(app))
    app.stopLabelFrame()
    app.stopTab()
    app.stopTabbedFrame()
    print("Registering Events")
    # app.registerEvent(motorStatusMonitor(app, Messenger)) #listen for the status changes
    app.registerEvent(lambda: UI.colorMode(app, "colorMode")) #Listen for changes to the colormode buttons
    def _close(app, arduino):
        res = app.yesNoBox("Confirm Exit", "Are you sure you want to exit?")
        if res:
            arduino.close()
        return res
    app.setStopFunction(lambda *a: _close(app, board))
    print("app is alive")
    app.go()
