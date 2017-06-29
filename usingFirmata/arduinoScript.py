from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
from toolz.curried import get, assoc, map, filter, reduce
import sys
import signal
from copy import deepcopy
from time import monotonic

LEONARDO=True
LOW = 0
HIGH = 1
INPUT_PULLUP = 0x0b




for item in [x for x in dir(Constants) if not(x.startswith("_"))]:
    exec(f"{item}=Constants.{item}")
global board
global pins
global buttons
global TIME
TIME = 1 #seconds
pins = {
    "motorAF_neutral": (9, OUTPUT),
    "motorAF_hot": (8, OUTPUT),
    "motorAR_neutral": (12, OUTPUT),
    "motorAR_hot": (11, OUTPUT),
    "motorBF_neutral": (2, OUTPUT),
    "motorBF_hot": (3, OUTPUT),
    "motorBR_neutral": ( 6, OUTPUT),
    "motorBR_hot": (5, OUTPUT),
    "buttonAF": (10, INPUT),
    "buttonAR": (13, INPUT),
    "buttonBF": (4, INPUT),
    "buttonBR": (7, INPUT)}


for name,(pinNumber, pinMode) in pins.items():
    exec(f"global {name}")
    exec(f"{name}={pinNumber}")

buttons= {"AF":buttonAF, "AR":buttonAR,"BF": buttonBF, "BR":buttonBR}
buttonState = [0]*4
currentState = [0]*4

def _signal_handler(sig, frame):
    if board is not None:
        print("\nYou pressed Ctrl+C")
        sys.exit(1)

signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)
if not sys.platform.startswith('win32'):
    signal.signal(signal.SIGALRM, _signal_handler)


def setup(board):
    global pins
    global buttons
    for name,(pinNumber, pinMode) in pins.items():
        if pinMode not in [INPUT, INPUT_PULLUP]:
            board.set_pin_mode(pinNumber, pinMode)
            board.digital_write(pinNumber, 0)
        else:
            board.set_pin_mode(pinNumber, pinMode)
            board.digital_write(pinNumber, 1)


def getButtons(board):
    global buttons
    return [board.digital_read(pin) for name,pin in buttons.items()]

def motorOff(board, motor):
    global pins
    if motor=="A":
        for name, (pin, setting) in pins.items():
            if name.startswith("motorA"):
                board.digital_write(pin, LOW)
    elif motor == "B":
        for name, (pin, setting) in pins.items():
            if name.startswith("motorB"):
                board.digital_write(pin, LOW)

def motorOn(board, motor, dir, delayTime=TIME):
    global pins
    if motor == "A":
        if dir == "F":
            for name, (pin, setting) in pins.items():
                if name.startswith("motorAR"):
                    board.digital_write(pin, LOW)
                if name.startswith("motorAF"):
                    board.digital_write(pin, HIGH)
        elif dir =="R":
            for name, (pin, setting) in pins.items():
                if name.startswith("motorAF"):
                    board.digital_write(pin, LOW)
                if name.startswith("motorAR"):
                    board.digital_write(pin, HIGH)
    elif motor=="B":
        if dir == "F":
            for name, (pin, setting) in pins.items():
                if name.startswith("motorBR"):
                    board.digital_write(pin, LOW)
                if name.startswith("motorBF"):
                    board.digital_write(pin, HIGH)
        elif dir =="R":
            for name, (pin, setting) in pins.items():
                if name.startswith("motorBF"):
                    board.digital_write(pin, LOW)
                if name.startswith("motorBR"):
                    board.digital_write(pin, HIGH)
    board.sleep(delayTime)

def loop(board):
    global buttonState
    global currentState
    thisLoopStart = monotonic()
    buttonState = getButtons(board)
    for button, value in zip(buttons.keys(), buttonState):
        print(f"Button {button}:\t {value}")

    if buttonState[0] == HIGH:
        if not(board.digital_read(motorAR_hot) == HIGH or currentState[1] == HIGH) or buttonState[1] == HIGH:
            motorOn(board, "A", "F")

    if buttonState[1] == HIGH:
        if not(board.digital_read(motorAF_hot) == HIGH or currentState[0] == HIGH) or buttonState[0] == LOW:
            motorOn(board, "A", "R")
    if buttonState[0] == LOW and buttonState[1] == LOW:
        motorOff(board, "A")

    if buttonState[2] == HIGH:
        if not(board.digital_read(motorBR_hot) == HIGH or currentState[3] == HIGH) or buttonState[3] == LOW:
            motorOn(board, "B", "F")

    if buttonState[3] == HIGH:
        if not(board.digital_read(motorBF_hot) == HIGH or currentState[2] == HIGH) or buttonState[2] == LOW:
            motorOn(board, "B", "R")
    if buttonState[2] == LOW and buttonState[3] == LOW:
        motorOff(board, "B")

    if board.digital_read(motorAF_hot) == HIGH:
        print("A: FWD")
    elif board.digital_read(motorAR_hot) == HIGH:
        print("A: REV")
    else:
        print("A: OFF")

    if board.digital_read(motorBF_hot) == HIGH:
        print("B: FWD")
    elif board.digital_read(motorBR_hot) == HIGH:
        print("B: REV")
    else:
        print("B: OFF")
    if (monotonic() - thisLoopStart) >= TIME:
        currentState = deepcopy(buttonState)
    else:
        while (monotonic() - thisLoopStart) < TIME:
            board.sleep(0.01)
        currentState=deepcopy(buttonState)



if __name__ == "__main__":
    if LEONARDO:
        board = PyMata3(arduino_wait=0)
    else:
        board = PyMata3()
    try:
        setup(board)
        while True:
            loop(board)
    except RuntimeError:
        board.shutdown()
        sys.exit(0)
