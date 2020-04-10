from core.sys.constants import Constant
import colorsys
from core.vector import Vector
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

    def fill(self, colour, hsv=True, force=False):
        brightness = core.sys.var.brightness
        if hsv and len((colour)) < 3:
            colour = list(colour) 
            colour.append(1) for i in range(3-len(colour))
        else:
            hsv = colorsys.rgb_to_hsv(*(Vector(*colour) / 255))






Backlight = Backlight()
