import asyncio
import queue as queues

import core.error
from core.render.primative import Primative
from core.hw.key import Key
from core.input.keys import name as key_names
from core.input.keys import Key as KeyEnum
from core.render.window import Window
from core.interface import Interface

import traceback

__all__ = ["Render"]

class Render:

    def __init__(self, pipeline, home: "coro"):
        self.__pipeline = pipeline
        self.__home = home
        self.__active = Window()
        self.__window_stack = []
        self.__event_queue = queues.Queue()
        self.__executing = asyncio.Event()
        self.__executing.set()

        self.__set_active(self.__active)

    async def execute(self):
        await self.__executing.wait()
        try:
            self.__active.render()
            self.__pipeline.execute()
        except Exception as e:
            print(traceback.print_exception(e, e, e.__traceback__))
        if Interface.active():
            Interface.schedule(self.execute())

    def submit(self, obj: Primative):
        self.__pipeline.submit(obj)

    def change_stack(self, stack: list, active: Window) -> [Window,]:
        output = (self.__window_stack, self.__active)
        self.__window_stack = stack
        self.__set_active(active)
        return output

    async def window_focus(self, window: "Window"):
        self.disable()
        self.__window_stack.append(self.__active)
        await self.__active.hide()
        self.__set_active(window)
        await self.__active.show()
        self.enable()

    async def window_pop(self):
        self.disable()
        await self.__active.hide()
        self.__set_active(self.__window_stack.pop())
        await self.__active.show()
        self.enable()

    def __set_active(self, window: "Window"):
        self.__active = window
        try:
            while True:
                self.__event_queue.get(False)
        except queues.Empty: pass
        self.__bind_handles()
        self.template()

    def template(self):
        self.__pipeline.template(self.__active.template)

    def disable(self):
        self.__executing.clear()
    def enable(self):
        self.__executing.set()

    def initialize(self):
        Key.initialize()
        self.__pipeline.open()
    def terminate(self):
        Key.terminate()
        self.__pipeline.close()

    def window_finish(self):
        if not self.__window_stack:
            self.__home_cb(-1, "press")
            return True
        return False

    def __home_cb(self, ch, event):
        Interface.schedule(self.__home(ch))

    async def process(self):
        try:
            await self.__executing.wait()
            while True:
                func, event = self.__event_queue.get(False)
                Interface.schedule(func(event))
        except queues.Empty:
            if Interface.active():
                Interface.schedule(self.process())

    def __bind_handles(self):
        def wrap(key, handler, active: Window):
            key = key_names[key]
            async def event(event):
                try:
                    func = getattr(getattr(handler, event), key)
                except AttributeError: return
                try:
                    await func(None, active)
                except Exception as e:
                    print(f"EventError: {type(e).__name__}: {e}")
                    raise core.error.Event(e, key, event, handler, active)

            event.__qualname__ = f"{active.__class__.__qualname__}-{key}"

            def submit(ch, event_type):
                self.__event_queue.put((event, event_type))
            return submit

        for key in (KeyEnum.UP.value, KeyEnum.DOWN.value, KeyEnum.LEFT.value, KeyEnum.CENTRE.value, KeyEnum.RIGHT.value):
            Key.bind(key, wrap(key, self.__active._event_handler_, self.__active))
        Key.bind(KeyEnum.BACK.value, self.__home_cb)