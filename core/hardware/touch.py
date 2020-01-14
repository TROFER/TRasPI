try:
    from driver.gfxhat import touch
except ImportError as e:
    print(e)
    from core.hardware.dummy import touch

__all__ = ["Touch"]

class _Touch:

    def __init__(self):
        pass

    def bind(self, buttons, handler=None):
        touch.on(buttons, handler)

    def repeat(self, rate=None):
        if rate is None:
            touch.enable_repeat(False)
        else:
            touch.enable_repeat(False)
            touch.repeat_rate(rate)

    def led(self, button, index=False):
        touch.set_led(button, index)

Touch = _Touch()
