from core.asset.asset import Asset
import core.system

__all__ = ["Program"]

class Program(metaclass=Asset):

    def __init__(self):
        self._module = core.system.load.window("main", self._path)
        self._set_path = False

    def __repr__(self) -> str:
        return "<Asset: {}[{}] {} : {}>".format(self.__class__.__name__, self._name, self._path, self._module)

    @property
    def module(self):
        return self._module

    @property
    def window(self):
        return self._module.main

    def import_path(self):
        if self._set_path == False:
            self._set_path = True
            core.sys.load.import_path(self._path)
        else:
            self._set_path = False
            core.sys.load.import_path(self._path)
