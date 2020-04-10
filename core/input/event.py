class _MetaHandler(type):
    def __new__(cls, name, bases, dct):
        if "window" not in dct:
            raise TypeError
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        if cls.window is not None:
            cls.window._event_handler_ = cls
        del cls.window, dct["window"]
        return super().__init__(name, bases, dct)

class Handler(metaclass=_MetaHandler):

    window = None

    def event(func):
        if func.__name__ not in [""] and False: # in Keys:
            raise TypeError
        return func

    class press:
        pass

    class release:
        pass

    class held:
        pass