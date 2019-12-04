from core.render.enums import Button

__all__ = ["Handler"]

class _Handler(type):

    # def __new__(cls, name, bases, attrs):
    #     return super().__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        try:
            del cls.key, cls.window
        except AttributeError as e:
            raise AttributeError("'{}' must have Attribute '{}'".format(cls.__name__, e.args[0])) from None
        keys = attrs.pop("key")
        if not hasattr(keys, "__iter__"):
            keys = [keys]
        windows = attrs.pop("window")
        if not hasattr(windows, "__iter__"):
            windows = [windows]
        for window in windows:
            if window is None:
                continue
            for key in keys:
                if key is Button.NONE:
                    continue
                window._handles[key.value] = cls
        super().__init__(name, bases, attrs)

    # def __call__(cls, window, *args, **kwargs):
    #     return super().__call__(*args, **kwargs)

class Handler(metaclass=_Handler):

    key = Button.NONE
    window = None

    def __init__(self, window):
        self.window = window

    def press(self):
        return

    def release(self):
        return

    def hold(self):
        return
