__all__ = ["Config"]

class _MetaConfig(type):

    def __new__(cls, name, bases, dct):
        if "_callback" in dct:
            callbacks = dct["_callback"]
            del dct["_callback"]
        else:
            callbacks = {}
        _vars = {}
        for key, var in [(k,v) for k,v in dct.items() if k[0] != "_"]:
            callback = callbacks[key] if key in callbacks else lambda x: None
            del dct[key]
            _vars[key] = [var, callback]
        dct["__vars"] = _vars
        return super().__new__(cls, name, bases, dct)

    def __getattribute__(cls, name):
        try:
            return super().__getattribute__("__vars")[name][0]
        except KeyError:
            raise AttributeError

    def __setattr__(cls, name, value):
        try:
            attr = super().__getattribute__("__vars")[name]
        except KeyError:
            if name == "_set_cb_":
                super().__getattribute__("__vars")[value[0]][1] = value[1]
                return
            raise AttributeError
        attr[0] = value
        attr[1](value)

class Config(metaclass=_MetaConfig):
    pass