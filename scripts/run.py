import mag
import smbus2 as smbus
import numpy as np
import time
from collections import OrderedDict
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


bus = smbus.SMBus(1)
address = 0x3D

sensor = mag.HMC5883L(bus, address, magDeclination=-0.171624)


data = mag.getTimedData(getMethod=sensor.getBearing, numSamples=500, pollRate=75, pinTrigger=True, pin=4)
data = np.array(data)

print(mag.textSummary(data, angular=True, radians=False))
GPIO.cleanup()


