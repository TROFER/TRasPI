from ..interface import Interface
# from .load import load
from ..error import logging as log

class Program:

    def __init__(self, app):
        self.application = app
        self.window_stack = []
        self.window_active = None
        self._intervals = set()
        self._file = ""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<'{self.application.name}' in '{self._file}' {len(self.window_stack)}#{self.window_active}>"

    def create_interval_func(self, func: callable, delay: float=1, repeat: int=-1) -> Interface.interval:
        i = Interface.interval(func, delay, repeat)
        self._intervals.add(i)
        return i

    def _acquire(self, other: "Program"):
        self.application = other.application
        self.application._program = self
        self.window_active = other.window_stack
        self.window_active = other.window_active
        self._intervals = other._intervals
        self._file = other._file
        return self

    async def open(self):
        try:
            self.window_active = self.application.window()
        except Exception as e:
            self.window_active = None
            raise
        try:
            await self.application.open()
        except Exception as e:
            log.program.warning("Application threw an Error %s %s: %s", self, type(e).__name__, e, extra={"program_name": self.application.name})
            log.traceback.warning("%s", self)
    async def close(self):
        for interval in self._intervals:
            interval.cancel()
        self._intervals.clear()
        try:
            await self.application.close()
        except Exception as e:
            log.program.warning("Application threw an Error %s %s: %s", self, type(e).__name__, e, extra={"program_name": self.application.name})
            log.traceback.warning("%s", self)

    async def show(self):
        for interval in tuple(self._intervals):
            if interval._cancel:
                self._intervals.remove(interval)
            else:
                interval.resume()
        try:
            await self.application.show()
        except Exception as e:
            log.program.warning("Application threw an Error %s %s: %s", self, type(e).__name__, e, extra={"program_name": self.application.name})
            log.traceback.warning("%s", self)
    async def hide(self):
        for interval in self._intervals:
            interval.pause()
        try:
            await self.application.hide()
        except Exception as e:
            log.program.warning("Application threw an Error %s %s: %s", self, type(e).__name__, e, extra={"program_name": self.application.name})
            log.traceback.warning("%s", self)