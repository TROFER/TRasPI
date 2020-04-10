import asyncio
from core.controller import Interface

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
        print("WAITED")
        await Interface.application().render.window_pop(self)
        print("POPING MY GUY")
        return self.__finish

    def finish(self, value=None):
        print("Finishing in func", value)
        self.__finish = value
        self.__event.set()
        print("Set event")
        return value

    def render(self):
        pass

    async def show(self):
        pass