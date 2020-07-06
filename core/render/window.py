import asyncio
from ..interface import Interface
from ..asset.std import AssetPool
from ..error import logging as log

__all__ = ["Window"]

class Window:

    _event_handler_ = None
    template = AssetPool.template

    def __init__(self):
        super().__init__()
        self.__event = asyncio.Event()
        self.__finish = None

    def __repr__(self):
        return f"Window.{self.__module__}.{self.__class__.__qualname__}"

    def __await__(self):
        return self.focus().__await__()

    async def focus(self):
        log.debug("%s", self)
        await Interface.application().render.window_focus(self)
        await self.__event.wait()
        self.__event.clear()
        await Interface.application().render.window_pop()
        return self.__finish

    def finish(self, value=None):
        log.debug("%s", self)
        self.__finish = value
        if Interface.application().render.window_finish():
            return
        self.__event.set()
        return value

    def render(self):
        pass

    async def show(self):
        pass
    async def hide(self):
        pass