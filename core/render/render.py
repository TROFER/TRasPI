import asyncio
import queue as queues

import core.error
from core.render.primative import Primative
from core.hw.key import Key
from core.input.keys import name as key_names
from core.input.keys import Key as KeyEnum
from core.render.window import Window
from core.interface import Interface

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
        print("Render:", self.__active)
        self.__active.render()
        self.__pipeline.execute()
        if Interface.active():
            Interface.schedule(self.execute())

    def submit(self, obj: Primative):
        self.__pipeline.submit(obj)

    def change_stack(self, active: Window, stack: list) -> [Window,]:
        self.__disable()
        output = [*self.__window_stack, self.__active]
        self.__window_stack = stack
        self.__set_active(active)
        self.__enable()
        return output

    async def window_focus(self, window: "Window"):
        self.__disable()
        self.__window_stack.append(self.__active)
        await self.__active.hide()
        self.__set_active(window)
        await self.__active.show()
        self.__enable()

    async def window_pop(self):
        self.__disable()
        await self.__active.hide()
        self.__set_active(self.__window_stack.pop())
        await self.__active.show()
        self.__enable()

    def __set_active(self, window: "Window"):
        self.__active = window
        try:
            while True:
                self.__event_queue.get(False)
        except queues.Empty: pass
        self.__bind_handles()
        self.__pipeline.template = self.__active.template

    def __disable(self):
        self.__executing.clear()
    def __enable(self):
        self.__executing.set()

    def initialize(self):
        self.__pipeline.open()
    def terminate(self):
        self.__pipeline.close()

    def __home_cb(self, ch, event):
        Interface.schedule(self.__home())

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
        def wrap(key, handler):
            key = key_names[key]
            async def event(event):
                try:
                    func = getattr(getattr(handler, event), key)
                except AttributeError: return
                try:
                    await func(None, self.__active)
                except Exception as e:
                    raise core.error.Event(e, key, event, handler, self.__active)

            def submit(ch, event_type):
                self.__event_queue.put((event, event_type))
            return submit

        for key in (KeyEnum.UP.value, KeyEnum.DOWN.value, KeyEnum.LEFT.value, KeyEnum.CENTRE.value, KeyEnum.RIGHT.value):
            Key.bind(key, wrap(key, self.__active._event_handler_))
        Key.bind(KeyEnum.BACK.value, self.__home_cb)