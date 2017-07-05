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

Config = Dome.readConfig(configFile="./.config")
Port = Config["SerialPort"]
PollTime = Config["PollTime"]
BaudRate = Config["BaudRate"]


# print(dict(Config))

# def signalHandlerGenerator(board):
#     def _signal_handler(sig, frame):
#         nonlocal board
#         if board is not None:
#             board.close()
#             print("\nYou pressed Ctrl+C")
#             sys.exit(1)
#     return _signal_handler
# _signal_handler = signalHandlerGenerator(arduino)
# signal.signal(signal.SIGINT, _signal_handler)
# signal.signal(signal.SIGTERM, _signal_handler)
# if not sys.platform.startswith('win32'):
#     signal.signal(signal.SIGALRM, _signal_handler)

def messagingConstructor(port, baudrate):
    global arduino
    arduino = Dome.Control.startBoard(port, baudrate, dtr=False)
    global messenger
    messenger = Dome.Control.startMessenger(arduino, Dome.Control.COMMANDS)




try:

    MessagingThread = threading.Thread(name="Messenger", target=messagingConstructor, args=(Port, BaudRate))
    UIThread = threading.Thread(name="UI", target=Dome.demo, args=(arduino, messenger), kwargs={"MotorDefaultTime":PollTime}, daemon=True)
    MessagingThread.start()
    UIThread.start()
    MessagingThread.join()
    UIThread.join()
except RuntimeError:
    arduino.close()
    sys.exit(0)
except KeyboardInterrupt:
    arduino.close()
    sys.exit(0)
except BaseException:
    arduino.close()
    sys.exit(0)
