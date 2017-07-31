import hug
import hug.types as types
import numpy as np
import toolz.curried as tc
import toolz.curried.operator as op

@hug.cli()
@hug.get(examples="motor=A&dir=F&val=On&duration=1")
@hug.local()
def sendCommand(motor: types.text, dir: types.text, val: types.text, duration: types.number)->types.text:
    """Dummy Command for Testing"""
    return f"motor{val}, {motor}, {dir}, {duration};"

if __name__ == "__main__":
    sendCommand.interface.cli()