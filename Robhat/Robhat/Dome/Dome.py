# -*- coding: utf-8 -*-
from . import Sensors
from . import Control
from . import UI
from . import Macros
from .. import Data
from typing import Dict, Text, Any, List, Tuple, Callable, Union, NewType
from toolz.curried import get, merge
import appJar as aj
from math import ceil
import PyCmdMessenger as cmd
import configparser
import scipy.stats
import sys

try:
    import smbus2 as smbus
except:
    pass


def readConfig(configFile: Text="./.config") -> Dict[Text, Union[Text, float, int]]:
    """
    Reads a configuration file.

    Args:
        configFile (Text): Path to the configuration file of which to parse

    Returns:
        Returns a dictionary containing the fields of the config file,
        with some special paramaters extracted from the raw text.
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


def appGetBearing(
        sensor: Union[Sensors.I2CDevice, Sensors.HMC5883L],
        numSamples: int=75, pollRate: int=75, pin=4, pinTrigger=False) -> float:
    """
    Gets the current bearing of the sensor provided as the first argument.

    Args:
        sensor (Union[Sensors.I2CDevice, Sensors.HMC5883L]): the sensor device that needs to be polled
        numSamples (int): how many samples should we get?
        pollRate (int): How many times per second should we poll the sensor?
        pin (int): If we want to trigger based off of a pin, we need to know what pin we're using.
        pinTrigger (bool): Should we care about triggering from a pin?

    Returns:
        A float between 0.0 and 360.0 which is the circular average of the boxcar[n=5]-circular average of the data read.

    """
    data = Sensors.getTimedData(
        getMethod=sensor.getBearing, numSamples=numSamples, pollRate=pollRate,
        pin=pin, pinTrigger=pinTrigger)
    averages, *rest = Data.boxcar(data, carlength=5,
                                  func=lambda x: scipy.stats.circmean(
                                      x, low=0, high=360))
    return scipy.stats.circmean(averages[:-5], low=0, high=360)


def motorStatusMonitor(
        app: aj.appjar.gui, Messenger: cmd.PyCmdMessenger.CmdMessenger,
        magSensor: Union[Sensors.I2CDevice, Sensors.HMC5883L]=None) -> Callable[[], None]:
    """
    Creates a callback that will update the GUI's status monitor with information.

    Args:
        app (aj.appjar.gui): What app interface to use?
        Messenger (cmd.PyCmdMessenger.CmdMessenger): Which messenger object to use?
        magSensor (Union[Sensors.I2CDevice, Sensors.HMC5883L]): What sensor to use to update the data, if any. If set to None, then skip the comparisons.

    Returns:
        getStatus (Callable[[],None]): A function that updates the status monitor's information based on the information it receives.

    """
    def getStatus() -> None:
        """
        Updates the status panel with the current information

        Returns:
            Nothing, this is a side-effect only function.
        """
        nonlocal Messenger
        nonlocal app
        nonlocal magSensor
        # Ask for the current status of the motor
        t = Control.sendCommand(Messenger, "kStatus")
        d = {t[1][0]: t[1][1], t[1][2]: t[1][3]}  # parse the response
        app.openTab("Main", "Control")
        app.openLabelFrame("Status")
        app.setLabel(
            "motorStatus",
            f"Motor A: \t {get('A', d, '???')}\nMotor B: \t {get('B', d, '???')}")
        if magSensor is not None:
            app.setLabel(
                "CurrentBearing",
                f"Current Bearing is: {appGetBearing(magSensor, numSamples=50, pollRate=75):.3f}°")
    return getStatus


def demo(board: cmd.arduino.ArduinoBoard,
         Messenger: cmd.PyCmdMessenger.CmdMessenger, *rest,
         MotorDefaultTime=1000, fullscreen=False, sensing=True) ->None:
    """

    Args:
        board (cmd.arduino.ArduinoBoard): what arduino object shuold we use?
        Messenger (cmd.PyCmdMessenger.CmdMessenger): What Messenger object is to be used?
        *rest: ignored.
        MotorDefaultTime (int): How long (in ms) should a motor be turned on if we press the button?
        fullscreen (bool): Should the app start in fullscreen mode?
        sensing (bool): Should we use the sensors?

    Returns:
        None, this is the main function that accesses the GUI.
    """

    def _close(app_: aj.appjar.gui, arduino_: cmd.arduino.ArduinoBoard) -> bool:
        """

        Args:
            app_ (aj.appjar.gui): get the main app object
            arduino_ (cmd.arduino.ArduinoBoard): get the main Arduino object.

        Returns:
            res (bool): Should we close the box or not? (True for Yes, False for No)
        """
        # res = app_.yesNoBox("Confirm Exit", "Are you sure you want to exit?")
        if True:#res:
            arduino_.close()
            sys.exit()
        return res

    def offBoth(*args, **kwargs) -> None:  # define a local function to turn off both motors
        """
        Sends a force off command to all motors and resets the radio buttons.

        Args:
            *args: ignored
            **kwargs: ignored

        Returns:
            None, this is a side-effect only function.
        """
        _0 = Control.sendCommand(Messenger, "kMotorOff", "A")
        del _0
        _1 = Control.sendCommand(Messenger, "kMotorOff", "B")
        del _1
        app.setRadioButton("AFControl", "Default", callFunction=False)
        app.setRadioButton("ARControl", "Default", callFunction=False)
        app.setRadioButton("BFControl", "Default", callFunction=False)
        app.setRadioButton("BRControl", "Default", callFunction=False)

    def motorRadioButtonChanged(button: Text) -> List[Union[Text, int, float, bool]]:
        """

        Args:
            button (Text): What appjar button are we listening for?

        Returns:
            response (List[Union[Text, int, float, bool]): The response we get back from the arduino board.
        """
        state = app.getRadioButton(button)
        if state == "Default":
            response = Control.sendCommand(Messenger, "kMotorOff", button[0])
            return response
        elif state == "FOn":
            val = "On"
        else:
            val = "Off"
        if button.startswith("A"):
            if val == "On":
                if button[1] == "F":
                    app.setRadioButton(
                        "ARControl", "Default", callFunction=False)
                    response = Control.sendCommand(
                        Messenger, "kMotorStayOn", "A", "F")
                elif button[1] == "R":
                    app.setRadioButton(
                        "AFControl", "Default", callFunction=False)
                    response = Control.sendCommand(
                        Messenger, "kMotorStayOn", "A", "R")
            else:
                Control.sendCommand(Messenger, "kMotorOff", "A")
        if button.startswith("B"):
            if val == "On":
                if button[1] == "F":
                    app.setRadioButton(
                        "BRControl", "Default", callFunction=False)
                    response = Control.sendCommand(
                        Messenger, "kMotorStayOn", "B", "F")
                elif button[1] == "R":
                    app.setRadioButton(
                        "BFControl", "Default", callFunction=False)
                    response = Control.sendCommand(
                        Messenger, "kMotorStayOn", "B", "R")
            else:
                response = Control.sendCommand(Messenger, "kMotorOff", "B")
        return response
    if sensing:
        bus = smbus.SMBus(1)
        address = 0x1e
        magSensor = Sensors.HMC5883L(bus, address, magDeclination=-0.171624)
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
    if sensing:
        app.addLabel(
            "CurrentBearing",
            f"Current Bearing is: {appGetBearing(magSensor, numSamples=50, pollRate=75):.3f}°")

    app.addButton(  # make me a button that turns off the motors!
        "offBoth",
        offBoth,
        3, 0, colspan=1, rowspan=1)
    app.stopLabelFrame()

    app.startLabelFrame("A", 1, 0, rowspan=2, colspan=1)
    print("making A")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onAF", lambda *a: Control.sendCommand(Messenger,
                                                         "kMotorOn", "A", "F", MotorDefaultTime), 0, 0)
    app.addButton("onAR", lambda *a: Control.sendCommand(Messenger,
                                                         "kMotorOn", "A", "R", MotorDefaultTime), 0, 1)
    app.addButton(
        "offA", lambda * a: Control.sendCommand(Messenger, "kMotorOff", "A"),
        1, 0, colspan=2, rowspan=1)

    app.stopLabelFrame()

    # app.startLabelFrame("ForcingA", 3, 0, colspan=1, rowspan=2)
    # 
    # app.startLabelFrame("AForward", 0, 0, colspan=1, rowspan=2)
    # app.addRadioButton("AFControl", "Default")
    # app.addRadioButton("AFControl", "FOn")
    # app.addRadioButton("AFControl", "FOff")
    # app.setRadioButton("AFControl", "Default", callFunction=False)
    # app.setRadioButtonChangeFunction("AFControl", motorRadioButtonChanged)
    # app.stopLabelFrame()
    # 
    # app.startLabelFrame("AReverse", 0, 1, colspan=1, rowspan=2)
    # app.addRadioButton("ARControl", "Default")
    # app.addRadioButton("ARControl", "FOn")
    # app.addRadioButton("ARControl", "FOff")
    # app.setRadioButton("ARControl", "Default", callFunction=False)
    # app.setRadioButtonChangeFunction("ARControl", motorRadioButtonChanged)
    # app.stopLabelFrame()
    # 
    # app.stopLabelFrame()

    app.startLabelFrame("B", 1, 2, rowspan=2, colspan=1)
    print("making B")
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("onBF", lambda *a: Control.sendCommand(Messenger,
                                                         "kMotorOn", "B", "F", MotorDefaultTime), 0, 0)
    app.addButton("onBR", lambda *a: Control.sendCommand(Messenger,
                                                         "kMotorOn", "B", "R", MotorDefaultTime), 0, 1)
    app.addButton(
        "offB", lambda * a: Control.sendCommand(Messenger, "kMotorOff", "B"),
        1, 0, colspan=2, rowspan=1)
    app.stopLabelFrame()

    # app.startLabelFrame("ForcingB", 3, 2, colspan=1, rowspan=2)

    # app.startLabelFrame("BForward", 0, 0, colspan=1, rowspan=2)
    # app.setSticky("nesw")
    # app.setStretch("both")
    # app.addRadioButton("BFControl", "Default")
    # app.addRadioButton("BFControl", "FOn")
    # app.addRadioButton("BFControl", "FOff")
    # app.setRadioButton("BFControl", "Default", callFunction=False)
    # app.setRadioButtonChangeFunction("BFControl", motorRadioButtonChanged)
    # app.stopLabelFrame()
    # 
    # app.startLabelFrame("BReverse", 0, 1, colspan=1, rowspan=2)
    # app.setSticky("nesw")
    # app.setStretch("both")
    # app.addRadioButton("BRControl", "Default")
    # app.addRadioButton("BRControl", "Force On")
    # app.addRadioButton("BRControl", "Force Off")
    # app.setRadioButton("BRControl", "Default", callFunction=False)
    # app.setRadioButtonChangeFunction("BRControl", motorRadioButtonChanged)
    # app.stopLabelFrame()
    # 
    # app.stopLabelFrame()

    app.stopTab()

    app.startTab("Macros")
    print("making Macros")
    app.setSticky("nesw")
    app.setStretch("both")

    app.startLabelFrame("Defaults", 0, 0, rowspan=2, colspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("Store", lambda *args: None, 0, 0, rowspan=1, colspan=2)
    app.addButton("Home", lambda *args: None, 1, 0, rowspan=1, colspan=2)
    app.stopLabelFrame()

    app.startLabelFrame("GUI", 0, 2, rowspan=2, colspan=2)
    app.setSticky("nesw")
    app.setStretch("both")
    app.addButton("Refresh", lambda *args: None, 0, 0, rowspan=1, colspan=2)
    app.addButton(
        "Exit", lambda *args: _close(app, board),
        1, 0, rowspan=1, colspan=2)
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
    # if sensing:
    # app.registerEvent(motorStatusMonitor(app, Messenger, magSensor=magSensor)) # listen for the status changes
    # else:
    # app.registerEvent(motorStatusMonitor(app, Messenger)) # Listen for status changes, no sensors.
    # Listen for changes to the colormode buttons
    app.registerEvent(lambda: UI.colorMode(app, "colorMode"))

    app.setStopFunction(lambda *a: _close(app, board))
    print("app is alive")
    app.go()
