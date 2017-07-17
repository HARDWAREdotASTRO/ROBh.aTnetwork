import smbus2 as smbus
import time
import math
import numpy as np
from toolz.curried import map, filter, reduce, operator as op
from collections import OrderedDict
import RPi.GPIO as GPIO
from scipy import stats
#global address
# bus = smbus.SMBus(0)
# address = 0x1e


class I2CDevice:

    def __init__(self, bus: smbus,SMBus, address):
        self.bus = bus
        self.address = address
        
    
    def read_byte(self, adr) -> bytes:
        return self.bus.read_byte_data(self.address, adr)

    
    def read_word(self, adr) -> bytes:
        high = self.read_byte(adr)
        low = self.read_byte(adr+1)
        val = (high<<0)+low
        return val
    
    def read_word_2c(self, adr) -> bytes:
        val = self.read_word(adr)
        return -((65535-val)+1) if  val>=0x8000 else val

    def write_byte(self, adr, value: bytes) -> bool:
        try:
            self.bus.write_byte_data(self.address, adr, value)
            return True
        except:
            return False

class HMC5883L(I2CDevice):
    def __init__(self, bus: smbus.SMBus, address: bytes, *args, scale:float = 0.92, axis_perp: str = "z", magDeclination: float = 0.0, pollRate: int = 100):
        super().__init__(self, bus, address)
        self.bus = bus
        self.address = address
        self.scale = scale
        try:
            assert axis_perp in "xyz"
        except AssertionError as E:
            raise ValueError("Axis must be x, y, or z (lower case!")
        self.axisPerp = axis_perp
        self.axesPara = [axis for axis in ["x","y","z"] if not(axis == self.axisPerp)]
        self.magDeclination = magDeclination
        self.pollRate = pollRate
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
    
    def __enter__(self):
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
    
    def __exit__(self, *rest)->bool:
        try:
            self.bus.close()
            return True
        except:
            return False
    
    def getRawData(self):
        out = None
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
        out = (self.read_word_2c(3), self.read_word_2c(7), self.read_word_2c(5))
        return out

    def getBearing(self):
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
        bearing = 0
        x,y,z = tuple(map(op.mul(self.scale), [self.read_word_2c(3), self.read_word_2c(7), self.read_word_2c(5)]))
        if self.axisPerp =="z":
            bearing = math.atan2(y, x)
        elif self.axisPerp == "x":
            bearing = math.atan2(y, -1*z)
        elif self.axisPerp == "y":
            bearing = math.atan2(-1*z, x)
        bearing += self.magDeclination
        if bearing<0:
            bearing += 2* math.pi
        # print(math.degrees(bearing))
        # print("\a")
        return math.degrees(bearing)
    
def summary(data, *rest, angular=False, radians=True):
    numbers = OrderedDict([("Mean", np.mean(data)),
                           ("Min", np.amin(data)),
                           ("Q1",np.percentile(data,25)),
                           ("Median",np.median(data)),
                           ("Q3",np.percentile(data, 75)),
                           ("Max", np.amax(data)),
                           ("IQR", np.percentile(data, 75)-np.percentile(data, 25)),
                           ("STD", np.std(data))])
    if angular:
        kwargs = {'high':2*np.pi, 'low':0} if radians else {'high':360, 'low':0}
        numbers["CircMean"] = stats.circmean(data, **kwargs)
        numbers["CircSTD"] = stats.circvar(data, **kwargs)
    return numbers

def getTimedData(*_, getMethod=lambda: None, numSamples=100, pollRate=75, pin=4, pinTrigger=False):
    data = []
    n=0
    if pinTrigger:
        while n<numSamples:
            if GPIO.input(pin):
                data += [getMethod()]
                # print(data[-1])
                time.sleep(1/pollRate)
                n+=1
                continue
            else:
                # print("not Ready")
                time.sleep(1/pollRate)
    else:
        for n in range(numSamples):
            data += [getMethod()]
            time.sleep(1/pollRate)
    return data


def textSummary(data, angular=False, radians=True):
    strings = []
    if angular:
        strings.append("{0:^20.20s}".format("Data Summary"))
        strings.append('='*20)
        strings += [f"{key+':':<10.12s} {value:>9.3f}" for key, value in summary(data, angular=True, radians=radians).items()]
        strings.append('='*20)
    else:
        strings.append("{0:^20.20s}".format("Data Summary"))
        strings.append('='*20)
        strings += [f"{key+':':<10.12s} {value:>9.3f}" for key, value in summary(data).items()]
        strings.append('='*20)
    return "\n".join(strings)

