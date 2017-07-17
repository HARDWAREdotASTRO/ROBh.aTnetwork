import time
import Adafruit_LSM303 as alm
import mag
import numpy as np
from scipy import stats
from collections import OrderedDict
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4, GPIO.IN)
GPIO.setup(5, GPIO.IN)

def name_of_object(arg):
    # check __name__ attribute (functions)
    try:
        return arg.__name__
    except AttributeError:
        pass

    for name, value in globals().items():
        if value is arg and not name.startswith('_'):
            return name


lsm303 = alm.LSM303()

data = mag.getTimedData(getMethod=lsm303.read, numSamples=500, pollRate=20, pinTrigger=True, pin=5)

data = np.array(data)

accels = data[:,0]
accels_x, accels_y, accels_z = accels[:,0].flatten(), accels[:,1].flatten(), accels[:,2].flatten()
mags = data[:,1]
mags_x, mags_y, mags_z = mags[:,0].flatten(), mags[:,1].flatten(), mags[:,2].flatten()

for thing in [accels_x, accels_y, accels_z, mags_x, mags_y, mags_z]:
    print(f"{name_of_object(thing)}:\n", mag.textSummary(thing, angular=False),'\n\n\n')
    
GPIO.cleanup()
