import sys
import os
from typing import Any, Iterable, Tuple
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
    platform = "NT" if os.name == "nt" else "UNIX"
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
            if name.startswith("__"):
                return super().__getattribute__(name)
            raise AttributeError

    def __setattr__(cls, name, value):
        try:
            var = super().__getattribute__("__vars")
            attr = var[name]
        except KeyError:
            if name == "_callback_":
                var[value[0]][1] = value[1]
                return
            raise AttributeError
        attr[0] = value
        attr[1](value)

    def __repr__(cls) -> str:
        return "<{} [{}]>".format(cls.__qualname__, ", ".join(f"{k}: {v[0]}" for k,v in super().__getattribute__("__vars").items()))

    def __iter__(self) -> Iterable[Tuple[str, Any]]:
        for k,v in super().__getattribute__("__vars").items():
            yield (k, v[0])

    def __getstate__(cls) -> dict:
        return super().__getattribute__("__vars")
    def __setstate__(cls, state: dict):
        var = super().__getattribute__("__vars")
        for key, value in state.items():
            var[key][0] = value

class Config(metaclass=_MetaConfig):
    pass

class SysConfig(Config):
    name = "Traspi"
    brightness = 65
    colour = 12
    volume = 75