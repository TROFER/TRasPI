from core.sys.constants import Constant
if Constant.pipeline == "GFXHAT":
    _FLAG = True
    from core.driver.gfxhat import backlight
else:
    _FLAG = False
    from core.driver.dummy import backlight

class Backlight:

    if _FLAG: # GXHAT

        def __init__(self):
            backlight.setup()

        def zone(self, zone: int, r: int, g: int, b: int):
            backlight.set_pixel(zone, r, g, b)

        def all(self, r: int, g: int, b: int):
            backlight.set_all(r, g, b)

        def show(self):
            backlight.show()

    else: # DUMMY

        def __init__(self):
            pass
        def zone(self, zone: int, r: int, g: int, b: int):
            pass
        def all(self, r: int, g: int, b: int):
            pass
        def show(self):
            pass


Backlight = Backlight()
