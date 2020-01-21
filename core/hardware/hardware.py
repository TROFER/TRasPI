try:
    from driver.gfxhat import backlight, touch, lcd
except ModuleNotFoundError:
    from core.hardware.dummy import backlight, touch, lcd
from core.sys.single import Singleton
from core.render.enums import Button as CoreButton
import colorsys

class Display:

    @classmethod
    def clear(cls):
        lcd.clear()
        cls.show()

    @classmethod
    def show(cls):
        lcd.show()

class Backlight:

    @classmethod
    def fill(cls, r, g, b):
        backlight.set_all(r, g, b)
        cls.show()

    @classmethod
    def gradient(cls, colours):
        for led in range(5):
            _colours = colorsys.hsv_to_rgb(colours[led] / 360, 1, 1)
            backlight.set_pixel(led, int(_colours[0]*255), int(_colours[1]*255), int(_colours[2]*255))
        cls.show()

    @classmethod
    def show(cls):
        backlight.show()

class Button:

    @classmethod
    def led(cls, value: bool, *led: CoreButton):
        if not led:
            led = (0, 1, 2, 3, 4, 5)
        for l in led:
            touch.set_led(l.value() if isinstance(l, CoreButton) else l, int(value))
