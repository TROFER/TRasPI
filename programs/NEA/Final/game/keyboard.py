import keyboard
import time

"""Wrapper for keyboard module to limit callrate"""

class Hotkey:

    def __init__(self, hotkey, callback, rate: float = 1):
        keyboard.add_hotkey(hotkey, self.call)
        self.callback = callback
        self.rate = rate
        self.lastpress = time.time()

    def call(self):
        if time.time() - self.lastpress > self.rate:
            self.callback()
            self.lastpress = time.time()


def unbind_all():
    keyboard.unbind_all()


keyboard = keyboard()
