from ..error.attributes import Constant, Config
from ..interface import Interface
from ..asset.res_pool import Pool
from ..asset.image import Image
from ..render.window import Window
from ..sys.program import Program
from ..sys.setting import Setting
from ..error import logging as log

__all__ = ["Application"]

def CreateWindow(window: Window):
    if isinstance(window, type):
        return window
    elif isinstance(window, Window):
        class WindowWrapper(Window):
            def __new__(cls):
                return window
        return WindowWrapper

class MetaApplication(type):
    def __init__(cls, name, bases, dct):

        if not issubclass(cls.var, Config):
            raise TypeError
        # core

        if not issubclass(cls.const, Constant):
            raise TypeError
        if not issubclass(cls.asset, Pool):
            raise TypeError

        if not isinstance(cls.settings, list):
            raise TypeError

        # Parse Settings
        def parse(settings: list):
            for setting in enumerate(settings):
                if isinstance(setting, list): # Sub Tree
                    # parse
                    pass

        try:
            if not issubclass(cls.window, Window):
                raise TypeError
            cls._program = Program(cls)
        except TypeError:
            raise TypeError("Must be Window Type") from None
        return super().__init__(name, bases, dct)

    def __repr__(self) -> str:
        return f"{self.__module__}['{self.name}']"
        # {len(self.asset)}

    # def __getattribute__(self):
    #     pass

class Application(metaclass=MetaApplication):

    name = "CoreApplicationTemplate"
    window = Window

    @classmethod
    def interval(self, func: callable, delay: float=1, repeat: int=-1) -> Interface.interval:
        """Calls func every 'delay' seconds 'repeat' number of times"""
        return self._program.create_interval_func(func, delay, repeat)

    class var(Config):
        pass

    class const(Constant):
        pass

    class asset(Pool):
        pass

    settings = []

    async def open():
        pass
    async def close():
        pass

    async def show():
        pass
    async def hide():
        pass