import numpy as np
import requests
import serial
from serial import Serial, SerialException
from toolz.curried import filter, get, map, reduce

from time import sleep
import os
import threading
# import asyncio
import configparser

from typing import Text

config = configparser.ConfigParser()
config.read(".config")

settings = config["DEFAULT"]
PollTime = int(settings["PollTime"])
SerialPort = settings["SerialPort"]
BaudRate = int(settings["BaudRate"])


def openConnection(port: Text = SerialPort, baudRate: int = BaudRate) -> Serial:
    return Serial(port, baudRate, timeout=PollTime / 1000)


con = openConnection(SerialPort, BaudRate)


def ensureConnected(con: Serial = con) -> bool:
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


def serialMonitor(con: Serial = con) -> None:
    """Prints out the received serial text"""
    ensureConnected(con)
    i = 0
    while True:
        try:
            print(f"{i:0>3d} | \t" + con.readline().decode("ascii"))
            i += 1
            i %= 1000
        except:
            os.abort()


def sendCommand(con: Serial = con, message: Text = "") -> None:
    """Send a message to the connection"""
    ensureConnected(con)
    con.write(message.encode("ascii"))


def get_input(con: Serial = con) -> None:
    """A stupidly simple REPL"""
    while True:
        try:
            print("Serial Command:")
            message = input(">>")
            print()
            sendCommand(con, message)
            # sleep(PollTime / 1000)
        except:
            os.abort()


def main(con: Serial = con) -> None:
    """Main function for the process"""
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


masterThread = threading.Thread(
    name="Master",
    target=main,
    args=(con,)
)
masterThread.start()
masterThread.join()
