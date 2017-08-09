# /home/pi/berryconda3/bin/python
# -*- coding: utf-8 -*-

import Robhat.Dome as Dome
import Robhat
import threading
import os
import sys

global Portglobal
global PollTime
global BaudRate
global arduino
global ThreadingQ
global SensingQ
global FullscreenQ

# ThreadingQ:
# False = No Threading
# True = Threads for App

ThreadingQ = True

# SensingQ:
# False = No Sensors
# True = Sensors used

SensingQ = False

FullscreenQ = True

Config = Dome.readConfig(configFile=r"sample.config")
Port = Config["SerialPort"]
PollTime = Config["PollTime"]
BaudRate = Config["BaudRate"]


# print(dict(Config))

try:
    arduino = Dome.Control.startBoard(Port, BaudRate, dtr=False)
    messenger = Dome.Control.startMessenger(arduino, Dome.Control.COMMANDS)
    if ThreadingQ:
        Dome.demo(arduino, messenger, MotorDefaultTime=PollTime, sensing=SensingQ, fullscreen=FullscreenQ)
    else:
        UIThread = threading.Thread(name="UI", target=Dome.demo, args=(arduino, messenger), kwargs={"fullscreen": FullscreenQ, "MotorDefaultTime":PollTime, "sensing": SensingQ}, daemon=True)
        UIThread.start()
        UIThread.join()

except (RuntimeError, KeyboardInterrupt, BaseException) as e:
    try:
        arduino.close()
        print(e)
        sys.exit(1)
    except:
        sys.exit(1)
