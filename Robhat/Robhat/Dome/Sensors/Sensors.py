import smbus2 as smbus
import time
import math
import numpy as np
from toolz.curried import operator as op
import importlib.util
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

class I2CDevice:

    def __init__(self, bus: smbus.SMBus, address):
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
        return math.degrees(bearing)



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
