from core.type.constant import Constant
from core.type.config import Config
from core.render.window import Window

class MetaProgram(type):

    def __init__(cls, name, bases, dct):
        if not issubclass(cls.var, Config):
            raise TypeError
        if not issubclass(cls.const, Constant):
            raise TypeError
        if not isinstance(cls.asset, dict):
            raise TypeError
        if not isinstance(cls.window, Window):
            raise TypeError
        return super().__init__(name, bases, dct)

class Program(metaclass=MetaProgram):

    class var(Config):
        pass

    class const(Constant):
        pass

    asset = {}
    window = Window()