class _MetaConfig(type):

    def __new__(cls, name, bases, dct):
        callbacks = dct["_callback"] if "_callback" in dct else {}
        _vars = {}
        for key, var in [(k,v) for k,v in dct.items() if k[0] != "_"]:
            callback = callbacks[key] if key in callbacks else lambda x: None
            del dct[key]
            _vars[key] = [var, callback]
        dct["__vars"] = _vars
        return super().__new__(cls, name, bases, dct)

    def __getattribute__(cls, name):
        return super().__getattribute__("__vars")[name][0]

    def __setattr__(cls, name, value):
        attr = super().__getattribute__("__vars")[name]
        attr[0] = value
        attr[1](value)

class Config(metaclass=_MetaConfig):
    pass

class SystemConfig(Config):
    _callback = {
        "brightness": lambda x: print("CB", x),

    }
    brightness = 1