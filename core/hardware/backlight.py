try:
    from driver.gfxhat import backlight
except ImportError as e:
    print(e)
        from core.hardware.dummy import backlight

__all__ = ["Backlight"]

class _Backlight:

    def __init__(self):
        pass

    def pixel(self, x, r, g, b):
        backlight.set_pixel(x, r, g, b)

    def all(self, r, g, b):
        backlight.set_all(r, g, b)

    def show(self):
        backlight.show()

Backlight = _Backlight()
