from toolz.curried import filter, get, map, reduce
from toolz.sandbox.core import unzip
import PyCmdMessenger as cmd
from time import sleep
import os
import threading
import configparser
import signal
from copy import copy, deepcopy
import sys

from typing import Any, Text, Dict, Sequence, List, Tuple, Callable, Union, NewType

global COMMANDS

COMMANDS = [["kMotorOn","ssi"],
            ["kMotorStayOn", "ss"],
            ["kMotorOff","s"],
            ["kStatus","s*"],
            ["kAck","s*"],
            ["kError","s*"],
            ["kLogging", "s*"]]


def startBoard(port: Text, baud: int = 9600, *args, dtr: bool = False) ->  cmd.arduino.ArduinoBoard:
    """Starts up a connection to the Arduino Board, it's basically a wrapper around a PySerial instance"""
    return cmd.ArduinoBoard(port, baud_rate=baud, enable_dtr=dtr)


def startMessenger(board: cmd.arduino.ArduinoBoard, commands_: List[List[Text]] = COMMANDS) -> cmd.PyCmdMessenger.CmdMessenger:
    """Starts up a CmdMessenger session"""
    return cmd.CmdMessenger(board, commands_, warnings=False)


def ensureConnected(board: cmd.arduino.ArduinoBoard) -> bool:
    """Make sure that the connection is active"""
    try:
        assert board.conneted
        return True
    except AssertionError:
        try:
            board.open()
            return True
        except:
            raise Exception("Bad connection object")


def serialMonitor(board: cmd.arduino.ArduinoBoard) -> None:
    """Prints out the received serial text"""
    ensureConnected(board)
    # i = 0
    while True:
        try:
            # print(f"{i:0>5d} | \t" + board.readline().decode("ascii"))
            # i += 1
            # i %= 10**5
            text = board.readline().decode("ascii")
            try:
                yield text
            except:
                pass
        except:
            # os.abort()
            pass


def listen(Messenger: cmd.PyCmdMessenger.CmdMessenger, messageIdentifier: Text, *rest, arg_format: Text = None, tries: int = 250) -> Any:
    """ Listens for a specific type of response message"""
    try:
        assert any([messageIdentifier in command for command in Messenger.commands])
        pass
    except:
        raise ValueError("Message identifier must be a valid command identifier for the Messenger")
    while True:
        if arg_format is not None:
            message = Messenger.receive(arg_formats=arg_format)
        else:
            message = Messenger.receive()

        if type(message) in [list, tuple] and message is not None:
            if message[0] == messageIdentifier:
                return message
            else:
                continue


# def getLogs(Messenger: cmd.PyCmdMessenger.CmdMessenger) -> Text:
#     """Yields the logs from the CmdMessenger"""
#     while True:
#         yield from listen(Messenger, "kLogging")


def sendCommand(Messenger: cmd.PyCmdMessenger, messageIdentifier: Text, *args) -> Any:
    """Sends a command and returns the response"""
    Messenger.send(messageIdentifier, *args)
    if messageIdentifier in [command for command in list(unzip(COMMANDS)[0])]:
        response = listen(Messenger, "kAck", "s*")
    else:
        response = listen(Messenger, "kError", "s*")
    return response
