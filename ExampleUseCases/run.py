import Robhat.Dome as Dome
import threading
import os
import sys
# import signal

global Portglobal
global PollTime
global BaudRate
global arduino
global _signal_handler
global ThreadingQ

# ThreadingQ:
# False = No Threading
# True = Threads for App

ThreadingQ = True

Config = Dome.readConfig(configFile="./.config")
Port = Config["SerialPort"]
PollTime = Config["PollTime"]
BaudRate = Config["BaudRate"]


# print(dict(Config))

try:
    arduino = Dome.Control.startBoard(Port, BaudRate, dtr=False)
    messenger = Dome.Control.startMessenger(arduino, Dome.Control.COMMANDS)
    if ThreadingQ:
        Dome.demo(arduino, messenger, MotorDefaultTime=PollTime, sensing=False)
    else:
        UIThread = threading.Thread(name="UI", target=Dome.demo, args=(arduino, messenger), kwargs={"MotorDefaultTime":PollTime, "sensing": False}, daemon=True)
        UIThread.start()
        UIThread.join()

except (RuntimeError, KeyboardInterrupt, BaseException) as e:
    try:
        arduino.close()
        print(e)
        sys.exit(1)
    except:
        sys.exit(1)
