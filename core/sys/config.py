from core.asset.asset import Asset
import json

class Config(metaclass=Asset):

    def __init__(self):
        try:
            self._config = json.load(open(self._path, 'r'))
        except IOError:
            print("No config file avalable")

    def __repr__(self) -> str:
        return "<Asset: {}[{}] {} : {}>".format(self.__class__.__name__, self._name, self._path, self._config)

    @property
    def config(self):
        return self._config

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

Config("std::system", path="system.cfg")
