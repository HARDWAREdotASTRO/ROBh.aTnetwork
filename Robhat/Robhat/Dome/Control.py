# -*- coding: utf-8 -*-
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

from typing import Any, Text, Dict, Sequence, List, Tuple, Callable, Union, NewType, Generator

global COMMANDS

COMMANDS = [["kMotorOn", "cci"],
            ["kMotorStayOn", "cc"],
            ["kMotorOff", "c"],
            ["kStatus", "s*"],
            ["kAck", "s*"],
            ["kError", "s*"],
            ["kLogging", "s*"]]
"""List[List[Text]]:
    A list of all commands possibly sent/recieved from the Arduino.
    The first slot is the name of the command.
    The second slot is the type-identifier of the command. See PyCmdMessenger's docs for details."""


def startBoard(port: Text, baud: int = 9600, *args, dtr: bool = False) -> cmd.arduino.ArduinoBoard:
    """
    A thin init function that binds to the PyCmdMessenger Arduino board class.

    Args:
        port (Text): What Serial Port should we bind to?
        baud (int): What's the baud rate?
        *args: ignored
        dtr (bool): Should we care about DTR?

    Returns:
        cmd.arduino.ArduinoBoard: the initialized ArduinoBoard object.

    """
    """Starts up a connection to the Arduino Board, it's basically a wrapper around a PySerial instance"""
    return cmd.ArduinoBoard(port, baud_rate=baud, enable_dtr=dtr)


def startMessenger(board: cmd.arduino.ArduinoBoard, commands_: List[List[Text]] = COMMANDS) -> cmd.PyCmdMessenger.CmdMessenger:
    """
    Starts up a CmdMessenger session (Thin wrapper around the PyCmdMessenger Messenger class constructor)

    Args:
        board (cmd.arduino.ArduinoBoard): What board object does the Messenger need to connect to?
        commands_ (List[List[Text]]): The commands that we need to pass to the Messenger class constructor.

    Returns:
        cmd.PyCmdMessenger.CmdMessenger: the initialized CmdMessenger object (ignores warnings!)
    """
    return cmd.CmdMessenger(board, commands_, warnings=False)


def ensureConnected(board: cmd.arduino.ArduinoBoard) -> bool:
    """
    Asserts that the connection is active

    Args:
        board (cmd.arduino.ArduinoBoard): What board to check

    Returns:
        bool: the status of the connection
    """
    try:
        assert board.conneted
        return True
    except AssertionError:
        try:
            board.open()
            return True
        except:
            raise Exception("Bad connection object")


def serialMonitor(board: cmd.arduino.ArduinoBoard) -> Generator[Text, None, None]:
    """
    Prints out the received serial text

    Args:
        board (cmd.arduino.ArduinoBoard): which board are we listening to?

    Returns:
        Generator[Text, None, None]: A generator instance that yields the raw responses

    """
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


def listen(
        Messenger: cmd.PyCmdMessenger.CmdMessenger, messageIdentifier: Text,
        *rest, arg_format: Text=None, tries: int=250) ->Any:
    """
    Listens for a specific type of response message.

    Args:
        Messenger (cmd.PyCmdMessenger.CmdMessenger): what messenger object should we use?
        messageIdentifier (Text): What type of message are we listening for?
        *rest: ignored.
        arg_format (Text): what format are the responses in? See PyCmdMessenger for details.
        tries (int): How many attempts should we listen to before quitting?

    Returns:

    """
    try:
        assert any([messageIdentifier in command
                    for command in Messenger.commands])
        pass
    except:
        raise ValueError(
            "Message identifier must be a valid command identifier for the Messenger")
    while True:
        if arg_format is not None:
            message = Messenger.receive(arg_formats=arg_format)
        else:
            message = Messenger.receive()

        if type(message) in [list, tuple] and message is not None:
            if message[0] == messageIdentifier:
                print(message)
                return message
            else:
                continue


def sendCommand(Messenger: cmd.PyCmdMessenger,
                messageIdentifier: Text, *args) -> List[Union[Text, int, float, bool]]:
    """
    Sends a command and returns the response.

    Args:
        Messenger (cmd.PyCmdMessenger.CmdMessenger): what messenger object should we use?
        messageIdentifier (Text): What message type should we send
        *args: the arguments we want to send, pass individually

    Returns:
        response (List[Union[Text, int, float, bool]]): the response we get back from the arduino.
    """
    Messenger.send(messageIdentifier, *args)
    if messageIdentifier in [command for command in list(unzip(COMMANDS)[0])]:
        response = listen(Messenger, "kAck", "s*")
    else:
        response = listen(Messenger, "kError", "s*")
    return response
