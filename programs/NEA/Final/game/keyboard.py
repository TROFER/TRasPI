import time

from app import App

import keyboard

"""Wrapper for keyboard module to limit callrate and prevent doubble binding"""

_hotkeys = {}


class Hotkey:

    def __init__(self, hotkey, callback, rate_limit: float = False):
        try:
            keyboard.remove_hotkey(_hotkeys[hotkey])
        except KeyError:
            pass
        _hotkeys[hotkey] = keyboard.add_hotkey(hotkey, self.call)
        self.callback = callback
        self.rate_limit = rate_limit
        self.lastpress = time.time()
        if App.const.debug:
            print(
                f"[DEBUG] Binding Set key: '{hotkey}' to '{callback.__name__}'")

    def call(self):
        if self.rate_limit:
            if time.time() - self.lastpress > self.rate_limit:
                self.callback()
                self.lastpress = time.time()
        else:
            self.callback()
    
def clear_all():
    global _hotkeys
    for hotkey in _hotkeys.values():
        keyboard.remove_hotkey(hotkey)
    _hotkeys = {}