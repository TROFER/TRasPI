from ..error.attributes import SysConstant, SysConfig
from ..vector import Vector
if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
    from ..driver.gfxhat import backlight
else:
    _FLAG = False
    from ..driver.dummy import backlight

from ..interface import Interface
import colorsys


class Backlight:

    if _FLAG:  # GFXHAT

        def __init__(self):
            backlight.setup()

        def zone(self, zone: int, r: int, g: int, b: int):
            backlight.set_pixel(zone, r, g, b)

        def all(self, r: int, g: int, b: int):
            backlight.set_all(r, g, b)
            backlight.show()

        def show(self):
            backlight.show()

    else:  # DUMMY

        def __init__(self):
            pass

        def zone(self, zone: int, r: int, g: int, b: int):
            pass

        def all(self, r: int, g: int, b: int):
            pass

        def show(self):
            pass

    def __colour_to_rgb(self, colour, hsv, force):
        if not hasattr(colour, "__iter__"):
            colour = (colour,)
        if hsv:
            _hsv = Vector(*colour, *(100 for i in range(max(3-len(colour), 0))))
            _hsv = _hsv.map(Vector(1/360, 0.01, 0.01))
        else:
            _hsv = Vector(*colorsys.rgb_to_hsv(*(Vector(*colour) / 255)))
        if not force:
            _hsv = Vector(*_hsv[:-1], SysConfig.brightness * 0.01)
        rgb = colorsys.hsv_to_rgb(*_hsv)
        return (Vector(*rgb) * 255).int()

    def fill(self, colour, hsv=True, force=False):
        self.all(*self.__colour_to_rgb(colour, hsv, force))

    def gradient(self, colours, hsv=True, force=False):
        colours = [self.__colour_to_rgb(c, hsv, force) for c in colours]
        if len(colours) == 2:
            diff = (colours[0] - colours[1]) / 6
            for i in range(4, 0, -1):
                colour.insert(1, diff * i + colour[0])
        for i, led in enumerate(colours):
            self.zone(i, *led)

    def termintate(self):
        self.fill((0, 0, 0), force=True)
        self.show()

Backlight = Backlight()
Interface.termintate.schedule(Backlight.termintate)
