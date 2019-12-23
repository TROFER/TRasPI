try:
    from gfxhat import backlight, touch, lcd
except ModuleNotFoundError:
    from core.hardware.dummy import backlight, touch, lcd
from core.render.single import Singleton
from core.render.enums import Button as CoreButton
import colorsys

class Display(metaclass=Singleton):

    def clear():
        lcd.clear(), lcd.show()
        backlight.set_all(0, 0, 0), backlight.show()

class Backlight(metaclass=Singleton):

    def fill(r, g, b):
        backlight.set_all(r, g, b)
        backlight.show()

    def gradient(colours):
        for led in range(5):
            _colours = colorsys.hsv_to_rgb(colours[led] / 360, 1, 1)
            backlight.set_pixel(led, int(_colours[0]*255), int(_colours[1]*255), int(_colours[2]*255))
        backlight.show()

class Button(metaclass=Singleton):

    def set_led(value: bool, *led: CoreButton):
        if not led:
            led = (0, 1, 2, 3, 4, 5)
        for l in led:
            touch.set_led(l.value() if isinstance(l, CoreButton) else l, int(value))
