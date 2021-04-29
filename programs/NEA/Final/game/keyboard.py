import time
from string import ascii_lowercase

from app import App

import keyboard

"""Wrapper for keyboard module to limit callrate and prevent doubble binding"""

_hotkeys = {}


class Hotkey:

    def __init__(self, hotkey: str, callback: callable, arguments: list = [], rate_limit: float = False):
        try: 
            keyboard.remove_hotkey(_hotkeys[hotkey])
        except KeyError:
            pass
        _hotkeys[hotkey] = keyboard.add_hotkey(
            hotkey, self.call, args=[arguments])
        self.callback = callback
        self.rate_limit = rate_limit
        self.lastpress = time.time()
        if App.const.debug:
            print(
                f"[DEBUG] - Binding Set key: '{hotkey}' to '{callback.__name__}'")

    def call(self, arguments=None, *args):
        if self.rate_limit:
            if time.time() - self.lastpress > self.rate_limit:
                if arguments:
                    self.callback(*arguments)
                else:
                    self.callback()
                self.lastpress = time.time()
        else:
            if arguments:
                self.callback(*arguments)
            else:
                self.callback()


def clear_all():
    """Clears all previously set hotkeys"""
    global _hotkeys
    for hotkey in _hotkeys.values():
        keyboard.remove_hotkey(hotkey)
    _hotkeys = {}


def all_alpha(callback: callable):
    """Creates alpha input, keypresses call the callback"""
    Hotkey("del", callback, arguments=["del"])
    for key in ascii_lowercase:
        if key != "j": # See Footnote
            Hotkey(key, callback, arguments=[key])

    # Key J is exculuded due to a bug in the keyboard module on linux where 'enter'
    # also calls the callback bound the the J key
