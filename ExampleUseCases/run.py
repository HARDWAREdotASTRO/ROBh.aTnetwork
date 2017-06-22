import Robhat.Dome as rob
import threading
import os
import serial

# Config = rob.Serial.readConfig(configFile="./.config")
# Port = Config["SerialPort"]
# PollTime = Config["PollTime"]
# BaudRate = Config["BaudRate"]

# con = Serial.openConnection(port=Port, baudRate=BaudRate, timeout=PollTime/1000)
con=serial.Serial()
# print(dict(Config))


# Term = lambda: rob.Serial.startTerminal(con)

# TermThread = threading.Thread(name="Terminal", target=Term, args=tuple())
UIThread = threading.Thread(name="UI", target=rob.demo, args=(con,))

try:
	# TermThread.setDaemon(True)
	UIThread.setDaemon(True)
	# TermThread.start()
	UIThread.start()
	# TermThread.join()
	UIThread.join()
except:
	os.abort()
