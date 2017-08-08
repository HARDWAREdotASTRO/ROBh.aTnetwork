# -*- coding: utf-8 -*-
import time
import math
import numpy as np
from toolz.curried import operator as op
import importlib.util
from typing import Union, Text, NewType, List, Callable, Tuple
try:
    importlib.util.find_spec('RPi.GPIO')
    importlib.util.find_spec('smbus2 ')
    import smbus2 as smbus
    import RPi.GPIO as GPIO
except ImportError:
    from fake_rpi import GPIO, smbus

I2C_Address = NewType("I2C_Address", Union[bytes, int])


class I2CDevice:
    """
    An object for interacting with i2c devices.

    Attributes:
        bus (smbus.SMBus): the bus for the current i2c device
        address (I2C_Address): The hex address of the current i2c device

    Args:
        bus (smbus.SMBus): the bus we're using to get the i2c device
        address (I2C_Address): The hex address of the device. (i.e. 0x0e or somthing similar)
    """

    def __init__(self, bus: smbus.SMBus, address: int):
        self.bus = bus
        self.address = address

    def __repr__(self) -> Text:
        """
        How python handles `print` method on this class.

        Returns:
            The representation of the object
        """
        return f"{self.__class__.__name__}({self.bus!r}, {self.address!r})"

    def __str__(self) -> Text:
        """
        How python handles string conversion of this class

        Returns:
            same as `__repr__`
        """
        return repr(self)

    def read_byte(self, adr: I2C_Address) -> bytes:
        """
        Read a byte from the i2c device.

        Args:
            adr (I2C_Address): The location to read the data from

        Returns:
            (bytes): The data from i2c device @adr.
        """
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr: I2C_Address) -> bytes:
        """
        Read a word from the i2c device

        Args:
            adr (I2C_Address): Where to start reading a word

        Returns:
            val (bytes): A word starting at adr
        """
        high = self.read_byte(adr)
        low = self.read_byte(adr + 1)
        val = (high << 0) + low
        return val

    def read_word_2c(self, adr: I2C_Address) -> bytes:
        """
        Read a word with some conversions

        Args:
            adr (I2C_Address): where to start

        Returns:
            val (bytes): The converted values.
        """
        val = self.read_word(adr)
        return -((65535 - val) + 1) if val >= 0x8000 else val

    def write_byte(self, adr: I2C_Address, value: bytes) -> bool:
        """
        Write a byte to the I2C device

        Args:
            adr (I2C_Address): Where to write the byte
            value (bytes): What to write

        Returns:
            (bool): Success or failure of the write.
        """
        try:
            self.bus.write_byte_data(self.address, adr, value)
            return True
        except:
            return False


class HMC5883L(I2CDevice):
    """
    A class that implements methods for HMC5883L Compass sensor

    Attributes:
        bus (smbus.SMBus): what bus the compass is on
        address (I2C_Address): Where on the bus the compass lives
        scale (float): What scale the compass needs to be at to get good readings.
        axisPerp (Text): What axis is perpindicular to the sensor board.
        axisPara (List[Text]): Which axes are not perp. to the sensor board.
        magDeclination (float): What the magnetic declination is set to.
        pollRate (int): The poll rate for the sensor

    Args:
        bus (smbus.SMBus): where the compass is connected to.
        address (I2C_Address): The I2C address of teh compass.
        *args: rest are ignored
        scale (float): The scale to multiply all readings by to normalize them.
        axis_perp (Text): What axis is perp to the ground ("x", "y", or "z").
        magDeclination (float): enter the number from https://www.ngdc.noaa.gov/geomag-web/#declination converted to decimal degrees.
        pollRate (int): How many times per second should we connect to the compass?
        **kwargs: ignored
    """

    def __init__(
            self, bus: smbus.SMBus, address: I2C_Address, *args,
            scale: float=0.92, axis_perp: Text="z", magDeclination: float=0.0,
            pollRate: int=100, **kwargs):
        super().__init__(self, bus, address)
        self.bus = bus
        self.address = address
        self.scale = scale
        try:
            assert axis_perp in "xyz"
        except AssertionError as E:
            raise ValueError("Axis must be x, y, or z (lower case!")
        self.axisPerp = axis_perp
        self.axesPara = [axis for axis in ["x", "y", "z"]
                         if not(axis == self.axisPerp)]
        self.magDeclination = magDeclination
        self.pollRate = pollRate
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)

    def __enter__(self):
        """
        Sets up the Sensor for use with ``with sensor as s:...`` magics!
        Also sets up the Sensor for use.

        Returns:
            None
        """
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)

    def __exit__(self, *rest)->bool:
        """
        Closes the connection

        Args:
            *rest: ignored

        Returns:
            (bool): Whether we were successfully able to disconnect from the compass (standard from the ``with sensor as s`` paradigm)
        """
        try:
            self.bus.close()
            return True
        except:
            return False

    def __repr__(self) -> Text:
        """
        How python handles ``print`` method on this class.

        Returns:
            The representation of the object
        """
        ret = f"{self.__class__.__name__}(" + \
              f"{self.bus!r}, " + \
              f"{self.address!r}, " + \
              f"scale={self.scale!r}, " + \
              f"axis_perp={self.axisPerp!r}, " +\
              f"magDeclination={self.magDeclination!r}" + \
              f"pollRate={self.pollRate!r})"
        return ret

    def __str__(self) -> Text:
        """
        How python handles string conversion of this class

        Returns:
            same as ``__repr__``
        """
        return repr(self)

    def getRawData(self) -> Tuple[bytes, bytes, bytes]:
        """

        Returns:
            out (Typle[bytes, bytes, bytes]): The x,y,z components of the current reading.
        """
        out = None
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
        out = (
            self.read_word_2c(3),
            self.read_word_2c(7),
            self.read_word_2c(5))
        return out

    def getBearing(self) -> float:
        """
        Gets the current bearing from the compass. Does NOT do any averaging, rather, we just process the raw data with ``math.atan2``

        Returns:

        """
        self.write_byte(0, 0b01110000)
        self.write_byte(1, 0b00100000)
        self.write_byte(2, 0b00000000)
        bearing = 0
        x, y, z = tuple(map(op.mul(self.scale), [self.read_word_2c(
            3), self.read_word_2c(7), self.read_word_2c(5)]))
        if self.axisPerp == "z":
            bearing = math.atan2(y, x)
        elif self.axisPerp == "x":
            bearing = math.atan2(y, -1 * z)
        elif self.axisPerp == "y":
            bearing = math.atan2(-1 * z, x)
        bearing += self.magDeclination
        if bearing < 0:
            bearing += 2 * math.pi
        return math.degrees(bearing)


def getTimedData(*_, getMethod: Callable[[],
                                         Union[float, int]]=lambda: None,
                 numSamples: int=100, pollRate: int=75, pin: int=4,
                 pinTrigger: bool=False) ->List[Union[int, float]]:
    """
    Get a time-series of data.

    Args:
        *_: all arguments MUST be supplied as keywords to this function.
        getMethod (Callable[],Union[float,int]): a function that when called with no arguments, returns a numeric response
        numSamples (int): How many samples should we get?
        pollRate (int): How many times per second should we get a sample?
        pin (int): Which pin should we watch for a signal on to get a sample?
        pinTrigger (bool): Should we even care about the pin?

    Returns:
        data (List[Union[int, float]]): A list of numeric data of length ``numSamples`` obtained by ``getMethod``.
    """
    data = []
    n = 0
    if pinTrigger:
        while n < numSamples:
            if GPIO.input(pin):
                data += [getMethod()]
                # print(data[-1])
                time.sleep(1 / pollRate)
                n += 1
                continue
            else:
                # print("not Ready")
                time.sleep(1 / pollRate)
    else:
        for n in range(numSamples):
            data += [getMethod()]
            time.sleep(1 / pollRate)
    return data
