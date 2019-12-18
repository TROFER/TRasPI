try:
    from gfxhat import backlight, touch
except ModuleNotFoundError:
    from core.hardware.dummy import backlight, touch
from core.render.single import Singleton
from core.render.enums import Button as CoreButton

class Backlight(metaclass=Singleton):

    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def fill(r, g, b):
        backlight.set_all(r, g, b)
        backlight.show()

    def gradient(colours):
        for led in range(5):
            print(colours[led] / 100)
            _colours = self.hsv_to_rgb(colours[led] / 100, 1, 1)
            print((int(_colours[0]*100), int(_colours[1]*100), int(_colours[2]*100)))
            backlight.set_pixel(led, int(_colours[0]*100), int(_colours[1]*100), int(_colours[2]*100))
        backlight.show()

class Button(metaclass=Singleton):

    def set_led(value: bool, *led: CoreButton):
        if not led:
            led = (0, 1, 2, 3, 4, 5)
        for l in led:
            touch.set_led(l.value() if isinstance(l, CoreButton) else l, int(value))
