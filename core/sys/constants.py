import sys
import os

class MetaConstant(type):

    def __delattr__(self, attr):
        raise AttributeError("Can not modify Constants")

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError("Can not modify Constants")
        super().__setattr__(name, value)

class Constant(metaclass=MetaConstant):
    width = 128
    height = 64
    path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
    platform = "NT" if os.name == "nt" else "POSIX"
    pipeline = "GFXHAT" # "GFXHAT" or "DUMMY"