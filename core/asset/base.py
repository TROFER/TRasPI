import os.path
from core.sys.attributes import SysConstant

__all__ = ["Asset"]

class _MetaAsset(type):
    def __new__(cls, name, bases, dct):
        paths = (SysConstant.path+"core/resource/"+name.lower()+"/", SysConstant.path+"programs/resource/"+name.lower()+"/",)
        dct["_prefix_paths"] = paths
        return super().__new__(cls, name, bases, dct)

class Asset(metaclass=_MetaAsset):

    def __init__(self, path: str):
        for prefix in self.__class__._prefix_paths:
            filepath = f"{prefix}{path}.{self.__class__.__name__.lower()}"
            if os.path.exists(filepath):
                self.path = filepath
                return
        raise FileNotFoundError

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            return super().__setattr__(name, value)
        raise TypeError("CONST")

    def __eq__(self, other) -> bool:
        return self.path == other.path
    def __ne__(self, other) -> bool:
        return self.path != other.path

    def __repr__(self) -> str:
        return f"Asset[{self.__class__.__name__}]"