import keyboard

class Keyboard:

    def __init__(self, parent: object, hotkeys: list, callbacks: list):
        self.parent = parent
        for i, hotkey in enumerate(hotkeys):
            keyboard.add_hotkey(hotkey, callbacks[i])