import serial
from serial import Serial, SerialException
from toolz.curried import filter, get, map, reduce

from time import sleep
import os
import threading
import configparser

from typing import Any, Text, Dict, Sequence, List, Tuple, Callable, Union, NewType


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


def openConnection(*, port: Text = "/dev/ttyACM0", baudRate: int = 9600, timeout: Union[int,float] = 5) -> Serial:
    """
    Opens a serial connection. all arguents are required to be passed as keywords
     Paramaters:
        port (Text): which port to use
        bautdRate (int): what baud Rate to use
    """

    return Serial(port, baudRate, timeout=timeout)


def ensureConnected(con: Serial) -> bool:
    """Make sure that the connection is active"""
    try:
        assert con.is_open
        return True
    except AssertionError:
        try:
            con.open()
            return True
        except:
            raise SerialException("Bad connection object")


def serialMonitor(con: Serial) -> None:
    """Prints out the received serial text"""
    ensureConnected(con)
    # i = 0
    while True:
        try:
            # print(f"{i:0>5d} | \t" + con.readline().decode("ascii"))
            # i += 1
            # i %= 10**5
            text = con.readline().decode("ascii")
            try:
                yield text
            except:
                pass
        except:
            # os.abort()
            pass


def sendCommand(con: Serial, *rest, message: Text = "") -> None:
    """Send a message to the connection
    Paramaters:
        con (Serial): a serial connection
        message (Text): the message to be sent (STRING)
    message is required to be given as a keyword argument
    """
    ensureConnected(con)
    con.write((message + "&").encode("ascii"))


def get_input(con: Serial) -> None:
    """A stupidly simple REPL"""
    while True:
        try:
            print("Serial Command:")
            message = input(">>")
            print()
            sendCommand(con, message=message)
            # sleep(PollTime / 1000)
        except:
            os.abort()


def startTerminal(con: Serial) -> None:
    """Main function for the process, starts a silly Serial Terminal"""
    monitorThread = threading.Thread(
        name="Monitor",
        target=serialMonitor,
        args=(con,)
    )
    commandThread = threading.Thread(
        name="Commands",
        target=get_input,
        args=(con,)
    )
    try:
        monitorThread.setDaemon(True)
        commandThread.setDaemon(True)
        monitorThread.start()
        commandThread.start()
        monitorThread.join()
        commandThread.join()
    except:
        os.abort()
