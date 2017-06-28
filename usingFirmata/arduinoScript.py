from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from toolz.curried import get, assoc, map, filter, reduce

for item in [x for x in dir(Constants) if not(x.startswith("_"))]:
    exec(f"{item}=Constants.{item}")

global board
global pins
global buttons
pins = {
    "motorAF_neutral" : (9, OUTPUT)
    "motorAF_hot" : (8, OUTPUT)
    "motorAR_neutral": (12, OUTPUT)
    "motorAR_hot": (11, OUTPUT)
    "motorBF_neutral" : (2, OUTPUT)
    "motorBF_hot" : (3, OUTPUT)
    "motorBR_neutral" :( 6, OUTPUT)
    "motorBR_hot" : (5, OUTPUT)
    "buttonAF": (10, INPUT)
    "buttonAR": (13, INPUT)
    "buttonBF" :(4, INPUT)
    "buttonBR" : (7, INPUT)}

buttons= {"AF":buttonAF, "AR":buttonAR,"BF": buttonBF, "BR":buttonBR}

for name,(pinNumber, pinMode) in pins.items():
    exec(f"global {name}")
    exec(f"{name}={pinNumber}")


def setup():
    global board
    global pins
    global buttons
    board = PyMata3(arduino_wait=0)
    for name,(pinNumber, pinMode) in pins.items():
        if pinMode != INPUT:
            board.set_pin_mode(pinNumber, pinMode)
            board.digitalWrite(pinNumber, 0)
        else:
            board.set_pin_mode(pinNumber, pinMode)
            board.digitalWrite(pinNumber, 1)


def getButtons():
    r = dict()
    for name,pin in buttons.items():
        r = assoc(r, name, board.digitalRead(pin))
    return r


if __name__ == "__main__":
    setup()
    while True:
        loop()
