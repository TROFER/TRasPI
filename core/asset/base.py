import os.path
from ..error.attributes import SysConstant
# from core.sys.attributes import SysConstant

__all__ = ["Asset"]

_search_paths = [SysConstant.path+"core/resource/", SysConstant.path, ""]
_active_dir = []

class _MetaAsset(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)

class Asset(metaclass=_MetaAsset):

    def __init__(self, path: str):
        search_paths = (*_search_paths, *_active_dir)
        name = self.__class__.__name__.lower()
        for prefix in search_paths:
            filepath = f"{prefix}{name}/{path}.{name}"
            if os.path.exists(filepath):
                self.path = filepath
                return
        p = "\n\t".join(_search_paths)
        raise FileNotFoundError(f"{path}.{name} in Directories:\n\t{p}")

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            return super().__setattr__(name, value)
        raise TypeError("Assets are Constant")

    def __eq__(self, other) -> bool:
        if isinstance(other, Asset):
            return self.path == other.path
        return False
    def __ne__(self, other) -> bool:
        if isinstance(other, Asset):
            return self.path != other.path
        return False

    def __repr__(self) -> str:
        return f"Asset[{self.__class__.__name__}]"