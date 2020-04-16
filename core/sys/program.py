from core.render.window import Window

from core.interface import Interface

class Program:

    def __init__(self, app):
        self.application = app
        self.window_stack = []
        self.window_active = app.window
        self._intervals = set()

    def create_interval_func(self, func: callable, delay: float=1, repeat: int=-1):
        self._intervals.add(Interface.interval(func, delay, repeat))

    async def main(self):
        pass

    async def open(self):
        print("Prog Open App")
        self.window_active = app.window
        await self.application.open()
    async def close(self):
        for interval in self._intervals:
            interval.cancel()
        self._intervals.clear()
        await self.application.close()

    async def show(self):
        print("resume intervals")
        for interval in self._intervals:
            interval.resume()
        print("Showing")
        await self.application.show()
    async def hide(self):
        for interval in self._intervals:
            interval.pause()
        await self.application.hide()