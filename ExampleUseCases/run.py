import Robhat.Dome as Dome
import threading
import os
import sys
# import signal
import asyncio as aio

global Portglobal
global PollTime
global BaudRate
global arduino
global _signal_handler

global ThreadingQ

# ThreadingQ:
# 0 = No Threading
# 1 = Only Threads for App
# 2 = Threads for app and messengers

ThreadingQ = 0

Config = Dome.readConfig(configFile="./.config")
Port = Config["SerialPort"]
PollTime = Config["PollTime"]
BaudRate = Config["BaudRate"]


# print(dict(Config))

try:
    arduino = Dome.Control.startBoard(Port, BaudRate, dtr=False)
    messenger = Dome.Control.startMessenger(arduino, Dome.Control.COMMANDS)
    if ThreadingQ == 0:
        Dome.demo(arduino, messenger, MotorDefaultTime=PollTime)
    elif ThreadingQ == 1:
        UIThread = threading.Thread(name="UI", target=Dome.demo, args=(arduino, messenger), kwargs={"MotorDefaultTime":PollTime}, daemon=True)
        UIThread.start()
        UIThread.join()
    elif ThreadingQ == 2:
        def messagingConstructor(port, baudrate):
            global arduino
            arduino = Dome.Control.startBoard(port, baudrate, dtr=False)
            global messenger
            messenger = Dome.Control.startMessenger(arduino, Dome.Control.COMMANDS)

        MessagingThread = threading.Thread(name="Messenger", target=messagingConstructor, args=(Port, BaudRate))
        UIThread = threading.Thread(name="UI", target=Dome.demo, args=(arduino, messenger), kwargs={"MotorDefaultTime":PollTime}, daemon=True)
        MessagingThread.start()
        UIThread.start()
        MessagingThread.join()
        UIThread.join()
    else:
        raise ValueError(f"ThreadingQ must be one of [0,1,2], got {ThreadingQ}")
except (RuntimeError, KeyboardInterrupt, BaseException) as e:
    arduino.close()
    raise e
    sys.exit(1)
