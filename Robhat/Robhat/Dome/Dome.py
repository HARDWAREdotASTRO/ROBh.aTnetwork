from . import Control, UI, Macros
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
from toolz.curried import get, merge
import appJar as aj
from math import ceil
import PyCmdMessenger as cmd
import configparser


def readConfig(configFile: Text = "./.config") -> Dict[Text, Union[Text, float, ]]:
    """
    Reads a configuration file.
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(configFile)
    settings = dict()
    settings["SerialPort"] = config["DEFAULT"]["SerialPort"]
    settings["PollTime"] = int(config["DEFAULT"]["PollTime"])
    settings["BaudRate"] = int(config["DEFAULT"]["BaudRate"])
    settings = merge(dict(config["DEFAULT"].items()), settings)
    return settings


def motorStatusMonitor(app: aj.appjar.gui, Messenger: cmd.PyCmdMessenger.CmdMessenger) -> Callable[[],None]:
    def getStatus()->None:
        nonlocal Messenger
        nonlocal app
        # Ask for the current status of the motor
        t = Control.sendCommand(Messenger, "kStatus")
        d = {t[1][0]: t[1][1], t[1][2]: t[1][3]}  # parse the response
        app.openTab("Main", "Control")
        app.openLabelFrame("Status")
        app.setLabel("motorStatus",
                     f"Motor A: \t {get('A', d, '???')}\nMotor B: \t {get('B', d, '???')}")

    return getStatus


def demo(board: cmd.arduino.ArduinoBoard, Messenger: cmd.PyCmdMessenger.CmdMessenger, *rest, MotorDefaultTime=1000,
         fullscreen=False) -> None:
    """Demo"""

    def _close(app_, arduino_) -> bool:
        res = app_.yesNoBox("Confirm Exit", "Are you sure you want to exit?")
        if res:
            arduino_.close()
        return res

    def offBoth(*args, **kwargs) -> None:  # define a local function to turn off both motors
        _0 = Control.sendCommand(Messenger, "kMotorOff", "A")
        del _0
        _1 = Control.sendCommand(Messenger, "kMotorOff", "B")
        del _1
        app.setRadioButton("AFControl", "Default", callFunction=False)
        app.setRadioButton("ARControl", "Default", callFunction=False)
        app.setRadioButton("BFControl", "Default", callFunction=False)
        app.setRadioButton("BRControl", "Default", callFunction=False)


    def motorRadioButtonChanged(button):
        state = app.getRadioButton(button)
        if state == "Default":
            response = Control.sendCommand(Messenger, "kMotorOff", button[0])
            return response
        elif state == "FOn":
            val = "On"
        else:
            val = "Off"
        if button.startswith("A"):
            if val=="On":
                if button[1]=="F":
                    app.setRadioButton("ARControl", "Default", callFunction=False)
                    response = Control.sendCommand(Messenger, "kMotorStayOn", "A", "F")
                elif button[1]=="R":
                    app.setRadioButton("AFControl", "Default", callFunction=False)
                    response = Control.sendCommand(Messenger, "kMotorStayOn", "A", "R")
            else:
                Control.sendCommand(Messenger, "kMotorOff", "A")
        if button.startswith("B"):
            if val == "On":
                if button[1] == "F":
                    app.setRadioButton("BRControl", "Default", callFunction=False)
                    response = Control.sendCommand(Messenger, "kMotorStayOn", "B", "F")
                elif button[1] == "R":
                    app.setRadioButton("BFControl", "Default", callFunction=False)
                    response = Control.sendCommand(Messenger, "kMotorStayOn", "B", "R")
            else:
                response = Control.sendCommand(Messenger, "kMotorOff", "B")
        return response

    app = UI.makeUI(size=(800, 480))
    app.setPollTime(ceil(1000 / MotorDefaultTime))
    if fullscreen:
        app.setGeometry("fullscreen")
    app.setSticky("nesw")
    app.setStretch("both")
    # app.setInPadding([25,25])
    # app.setPadding([20,20])

    app.startTabbedFrame("Main")
    app.startTab("Control")

    app.startLabelFrame("Status", 1, 1, colspan=1, rowspan=5)
    app.setSticky("nesw")
    app.setStretch("both")
    print("making status panel")
    app.addLabel("motorStatus", "Motor A: \t ??? \nMotor B: \t ???", 0, 0)


    app.addButton(  # make me a button that turns off the motors!
            "offBoth",
            offBoth,
            3, 0, colspan=1, rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("A", 1, 0, rowspan=2, colspan=1)
    print("making A")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onAF", lambda *a: Control.sendCommand(Messenger, "kMotorOn", "A", "F", MotorDefaultTime), 0, 0)
    app.addButton("onAR", lambda *a: Control.sendCommand(Messenger, "kMotorOn", "A", "R", MotorDefaultTime), 0, 1)
    app.addButton("offA", lambda *a: Control.sendCommand(Messenger, "kMotorOff", "A"), 1, 0, colspan=2, rowspan=1)


    app.stopLabelFrame()

    app.startLabelFrame("ForcingA", 3,0, colspan=1, rowspan=2)

    app.startLabelFrame("AForward", 0, 0, colspan=1, rowspan=2)
    app.addRadioButton("AFControl", "Default")
    app.addRadioButton("AFControl", "FOn")
    app.addRadioButton("AFControl", "FOff")
    app.setRadioButton("AFControl", "Default", callFunction=False)
    app.setRadioButtonChangeFunction("AFControl", motorRadioButtonChanged )
    app.stopLabelFrame()

    app.startLabelFrame("AReverse", 0, 1, colspan=1, rowspan=2)
    app.addRadioButton("ARControl", "Default")
    app.addRadioButton("ARControl", "FOn")
    app.addRadioButton("ARControl", "FOff")
    app.setRadioButton("ARControl", "Default", callFunction=False)
    app.setRadioButtonChangeFunction("ARControl", motorRadioButtonChanged)
    app.stopLabelFrame()

    app.stopLabelFrame()


    app.startLabelFrame("B", 1, 2, rowspan=2, colspan=1)
    print("making B")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Control.sendCommand(Messenger, "kMotorOn", "B", "F", MotorDefaultTime), 0, 0)
    app.addButton("onBR", lambda *a: Control.sendCommand(Messenger, "kMotorOn", "B", "R", MotorDefaultTime), 0, 1)
    app.addButton("offB", lambda *a: Control.sendCommand(Messenger, "kMotorOff", "B"), 1, 0, colspan=2, rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("ForcingB", 3, 2, colspan=1, rowspan=2)

    app.startLabelFrame("BForward", 0, 0, colspan=1, rowspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addRadioButton("BFControl", "Default")
    app.addRadioButton("BFControl", "FOn")
    app.addRadioButton("BFControl", "FOff")
    app.setRadioButton("BFControl", "Default", callFunction=False)
    app.setRadioButtonChangeFunction("BFControl", motorRadioButtonChanged)
    app.stopLabelFrame()

    app.startLabelFrame("BReverse", 0, 1, colspan=1, rowspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addRadioButton("BRControl", "Default")
    app.addRadioButton("BRControl", "Force On")
    app.addRadioButton("BRControl", "Force Off")
    app.setRadioButton("BRControl", "Default", callFunction=False)
    app.setRadioButtonChangeFunction("BRControl", motorRadioButtonChanged)
    app.stopLabelFrame()

    app.stopLabelFrame()

    app.stopTab()

    app.startTab("Macros")
    print("making Macros")
    app.setSticky("nesw")
    app.setStretch("both")

    app.startLabelFrame("Defaults", 0,0, rowspan=2, colspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("Store", lambda *args: None, 0,0, rowspan=1, colspan=2)
    app.addButton("Home", lambda *args: None, 1,0, rowspan=1, colspan=2)
    app.stopLabelFrame()

    app.startLabelFrame("GUI", 0, 2, rowspan=2, colspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("Refresh", lambda *args: None, 0,0, rowspan=1, colspan=2)
    app.addButton("Exit", lambda *args: _close(app, arduino), 1,0, rowspan=1, colspan=2)
    app.stopLabelFrame()

    app.stopTab()

    app.startTab("Settings")
    print("making settings")
    app.setSticky("nesw")
    app.setStretch("both")
    app.startLabelFrame("Display", 1, 0)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addRadioButton("colorMode", "Normal")
    app.addRadioButton("colorMode", "Night")
    app.setRadioButton("colorMode", "Normal", callFunction=False)
    app.setRadioButtonChangeFunction("colorMode", UI.colorMode(app))
    app.stopLabelFrame()
    app.stopTab()
    app.stopTabbedFrame()
    print("Registering Events")
    # Keep the status monitor commented out for now, it polls too frequently and blocks UI
    # app.registerEvent(motorStatusMonitor(app, Messenger)) # listen for the status changes
    app.registerEvent(lambda: UI.colorMode(app, "colorMode"))  # Listen for changes to the colormode buttons

    app.setStopFunction(lambda *a: _close(app, board))
    print("app is alive")
    app.go()
