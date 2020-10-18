from .keys import name as key_names
from ..render.window import Window

__all__ = ["Handler", "event"]

class _MetaHandler(type):

    def __new__(cls, name, bases, dct):
        windows = []
        base = []
        for b in bases:
            if issubclass(b, Window):
                windows.append(b)
            else:
                base.append(b)

        for handle_name in ("press", "release", "held"):
            handle = dct.get(handle_name, False)
            if handle:
                for name in key_names:
                    if not hasattr(handle, name):
                        for window in windows:
                            if hasattr(window._event_handler_, handle_name) and hasattr(getattr(window._event_handler_, handle_name), name):
                                setattr(handle, name, getattr(getattr(window._event_handler_, handle_name), name))
                                break

        return super().__new__(cls, name, tuple(base), dct)

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