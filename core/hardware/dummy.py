from core.render.single import Singleton
from core.sys import WIDTH, HEIGHT

__all__ = ["lcd", "touch", "backlight"]

class _lcd(metaclass=Singleton):

    def __init__(self):
        self.buffer = [["#" for y in range(HEIGHT)] for x in range(WIDTH)]

    def set_pixel(self, x, y, value):
        if value == 1:
            value = "-"
        else:
            value = "#"
        self.buffer[x][y] = value

    def show(self):
        for x in range(WIDTH):
            print(" ".join([self.buffer[x][y] for y in range(HEIGHT)]))

    def contrast(self):
        pass

class _touch(metaclass=Singleton):

    def __init__(self):
        pass

    def on(*args, **kwargs):
        pass

    def enable_repeat(self, enable: bool):
        pass

    def set_repeat_rate(self, rate: int):
        pass

class _backlight(metaclass=Singleton):

    def __init__(self):
        pass

    def set_all(self, r, g, b):
        pass

    def clear(self):
        pass

    def set_pixel(self, x, y, r, g, b):
        pass

#------------------------------------------------------------------------------#

lcd = _lcd()
touch = _touch()
backlight = _backlight()
