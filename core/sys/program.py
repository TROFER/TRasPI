# from core.render.window import Window
from core.interface import Interface

class Program:

    def __init__(self, app):
        self.application = app
        self.window_stack = []
        self.window_active = None
        self._intervals = set()
        self._file = ""

    def create_interval_func(self, func: callable, delay: float=1, repeat: int=-1):
        self._intervals.add(Interface.interval(func, delay, repeat))

    async def main(self):
        pass

    async def open(self):
        try:
            self.window_active = self.application.window()
        except Exception as e:
            self.window_active = None
            raise
        await self.application.open()
    async def close(self):
        for interval in self._intervals:
            interval.cancel()
        self._intervals.clear()
        await self.application.close()

    async def show(self):
        for interval in self._intervals:
            interval.resume()
        await self.application.show()
    async def hide(self):
        for interval in self._intervals:
            interval.pause()
        await self.application.hide()