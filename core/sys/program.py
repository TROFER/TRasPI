# from core.render.window import Window
from core.interface import Interface

class Program:

    def __init__(self, app):
        self.application = app
        self.window_stack = []
        self.window_active = None
        self._intervals = set()
        self._file = ""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self._file} {len(self.window_stack)}>{self.window_active} {self.application}>"

    def create_interval_func(self, func: callable, delay: float=1, repeat: int=-1):
        self._intervals.add(Interface.interval(func, delay, repeat))

    async def main(self):
        pass

    async def open(self):
        print("Opening")
        try:
            self.window_active = self.application.window()
        except Exception as e:
            self.window_active = None
            raise
        print("App Open")
        await self.application.open()
    async def close(self):
        print("Closing")
        for interval in self._intervals:
            interval.cancel()
        self._intervals.clear()
        print("App Close")
        await self.application.close()

    async def show(self):
        print("Showing")
        for interval in self._intervals:
            interval.resume()
        print("App Show", self)
        await self.application.show()
    async def hide(self):
        print("Hiding")
        for interval in self._intervals:
            interval.pause()
        print("App Hide")
        try:
            await self.application.hide()
        except Exception:
            pass