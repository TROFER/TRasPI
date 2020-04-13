import sys
import os
# from core.type.config import Config
# from core.type.constant import Constant

__all__ = ["SysConstant", "SysConfig"]

# __all__ = ["Constant"]

class MetaConstant(type):

    def __delattr__(self, attr):
        raise AttributeError("Can not modify Constants")

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("Can not modify Constants")
        super().__setattr__(name, value)

class Constant(metaclass=MetaConstant):
    pass

class SysConstant(Constant):
    width = 128
    height = 64
    path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
    platform = "NT" if os.name == "nt" else "POSIX"
    pipeline = "GFXHAT" # "GFXHAT" or "DUMMY"

# __all__ = ["Config"]

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

class SysConfig(Config):
    name = "Traspi"
    brightness = 65
    colour = 12