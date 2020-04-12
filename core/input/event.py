from core.input.keys import name as key_names
from core.render.window import Window

__all__ = ["Handler", "event"]

class _MetaHandler(type):

    def __init__(cls, name, bases, dct):
        if not issubclass(cls.window, Window):
            raise TypeError
        cls.window._event_handler_ = cls
        return super().__init__(name, bases, dct)

class Handler(metaclass=_MetaHandler):

    window = Window

    class press:
        pass

    class release:
        pass

    class held:
        pass

def event(func):
    if func.__name__ not in key_names:
        raise TypeError
    return func