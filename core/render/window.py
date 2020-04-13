import asyncio
from core.interface import Interface

__all__ = ["Window"]

class Window:

    _event_handler_ = None
    template = None

    def __init__(self):
        self.__event = asyncio.Event()
        self.__finish = None

    def __await__(self):
        return self.focus().__await__()

    async def focus(self):
        await Interface.application().render.window_focus(self)
        await self.__event.wait()
        await Interface.application().render.window_pop()
        return self.__finish

    def finish(self, value=None):
        self.__finish = value
        self.__event.set()
        return value

    def render(self):
        pass

    async def show(self):
        pass
    async def hide(self):
        pass