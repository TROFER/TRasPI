import core.error
from driver.gfxhat import lcd

__all__ = ["Display"]

class _Display:

    def __init__(self):
        lcd.st7567.setup()
        self.contrast(40) #Sets system contrast value #40 = default

    def clear(self):
        lcd.clear()
        self.show()

    def pixel(self, x, y, value):
        lcd.set_pixel(x, y, value)

    def show(self):
        lcd.show()

    def contrast(self, value=None):
        if value is not None:
            try:
                lcd.contrast(value)
                self._contrast_value = value
            except Exception as e:
                raise
        return self._contrast_value

Display = _Display()
