from core.sys.single import Singleton
import time

class DeltaTime(metaclass=Singleton):

    def __init__(self, value: float=0):
        self._value = value
        self.old = 0
        self.new = 0

    def __float__(self) -> float:
        return self._value

    @property
    def value(self):
        return self._value

    def next(self):
        self.old = self.new
        self.new = time.time()
        self._value = self.new - self.old
        return self._value