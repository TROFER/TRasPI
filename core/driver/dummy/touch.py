import threading
from core.driver.dummy import soutput

from core.interface import Interface

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
        if key == "q":
            __funcs[0](0, "press")
        if key == "a":
            __funcs[1](1, "press")
        if key == "z":
            __funcs[2](2, "press")
        if key == "x":
            __funcs[3](3, "press")
        if key == "c":
            __funcs[4](4, "press")
        if key == "v":
            __funcs[5](5, "press")

def setup():
    threading.Thread(target=__poll_loop).start()