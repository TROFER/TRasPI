from driver.gfxhat import lcd

__all__ = ["Display"]

class _Display:

    def __init__(self):
        pass

    def clear(self):
        lcd.clear()
        self.show()

    def pixel(self, x, y, value):
        lcd.set_pixel(x, y, value)

    def show(self):
        lcd.show()

    def contrast(self, value):
        lcd.contrast(value)

Display = _Display()
