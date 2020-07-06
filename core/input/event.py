from .keys import name as key_names
from ..render.window import Window

__all__ = ["Handler", "event"]

class _MetaHandler(type):

    def __init__(cls, name, bases, dct):
        if not issubclass(cls.window, Window):
            raise TypeError(f"Handler Must be Linked to a '{Window.__name__}' type. Not a '{cls.window.__name__}'")
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