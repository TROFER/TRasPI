from ..error.attributes import SysConstant
from time import sleep

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
    from ..driver.gfxhat import touch
    from ..driver.keyboard import keyboard
else:
    _FLAG = False
    from ..driver.dummy import touch

'''
if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
    from ..driver.gfxhat import touch
else:
    _FLAG = False
    from ..driver.dummy import touch
'''

class Key:

    if _FLAG:  # GFXHAT

        def __init__(self):
            touch.setup()

        def initialize(self):
            pass

        def terminate(self):
            pass

        def bind(self, button, function):
            touch.on(button, function)
            keyboard.bind(button, function)

        def repeat(self, rate=None):
            if rate is None:
                touch.enable_repeat(False)
            else:
                touch.enable_repeat(True)
                touch.set_repeat_rate(rate)

        def led(self, button, state=False):
            touch.set_led(button, state)

        def all(self, state=False):
            for button in range(0, 6):
                touch.set_led(button, state)

        def flash(self, speed: float = 1, repeats: int = 1):
            for repeat in range(0, repeats):
                self.all(1)
                sleep(speed)
                self.all(0)

    else:  # DUMMY

        def __init__(self):
            pass

        def initialize(self):
            touch.setup()

        def terminate(self):
            pass

        def bind(self, button, function):
            touch.bind(button, function)

        def repeat(self, rate=None):
            pass

        def led(self, button, state=False):
            pass

        def all(self, state):
            pass

        def flash(self, speed: float = 1, repeats: int = 1):
            pass


Key = Key()
