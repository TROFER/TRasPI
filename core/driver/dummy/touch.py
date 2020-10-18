import threading
from . import soutput

from ...interface import Interface

def __default(ch: int, event_type: str):
    print(ch, event_type)

__funcs = [__default] * 6

def bind(button: int, function: callable):
    __funcs[button] = function

def __poll_loop():
    while Interface.active():
        key = soutput.get_key()
        if not key:
            continue
        if key == "w":
            __funcs[0](0, "press")
        if key == "s":
            __funcs[1](1, "press")
        if key == "q":
            __funcs[2](2, "press")
        if key == "a":
            __funcs[3](3, "press")
        if key == "e":
            __funcs[4](4, "press")
        if key == "d":
            __funcs[5](5, "press")

def setup():
    threading.Thread(target=__poll_loop, name="Dummy-Touch").start()