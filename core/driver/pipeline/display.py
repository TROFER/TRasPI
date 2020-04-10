from core.sys.constants import Constant
if Constant.pipeline == "GFXHAT":
    _FLAG = True
    from core.driver.gfxhat import lcd as lcd
else:
    _FLAG = False
    from core.driver.dummy import lcd

class Display:

    if _FLAG: # GFXHAT
        def __init__(self):
            lcd.st7567.setup()
            self.contrast(40)

        def clear(self):
            lcd.clear()
            self.show()

        def pixel(self, x: int, y: int, value: int):
            lcd.set_pixel(x, y, value)

        def show(self):
            lcd.show()

        def contrast(self, value: int):
            lcd.contrast(value)

        def rotation(self, rotated=False):
            lcd.rotation(180 if rotated else 0)

    else: # DUMMY
        def __init__(self):
            lcd.setup()

        def clear(self):
            lcd.clear()
            self.show()

        def pixel(self, x: int, y: int, value: int):
            lcd.set_pixel(x, y, value)

        def show(self):
            lcd.show()

        def contrast(self, value: int):
            return

        def rotation(self, rotated=False):
            # DO THIS
            pass

Display = Display()
