try:
    from gfxhat import backlight, touch
except ModuleNotFoundError:
    from core.hardware.dummy import backlight, touch
from core.render.single import Singleton
from core.render.enums import Button as CoreButton

class Backlight(metaclass=Singleton):

    def fill(r, g, b):
        backlight.set_all(r, g, b)
        backlight.show()

    def gradient(colours):
        for led in range(5):
            _colours = [int(hex_colour, 16) for hex_colour in [colours[led][i:i + 2] for i in range(0, 6, 2)]]
            backlight.set_pixel(led, _colours[0], _colours[1], _colours[2])
        backlight.show()

class Button(metaclass=Singleton):

    def set_led(value: bool, *led: CoreButton):
        if not led:
            led = (0, 1, 2, 3, 4, 5)
        for l in led:
            touch.set_led(l.value() if isinstance(l, CoreButton) else l, int(value))
