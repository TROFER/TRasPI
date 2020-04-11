import queue as queues

from core.render.primative import Primative
from core.hw.key import Key
from core.input.keys import name as key_names
from core.render.window import Window
from core.interface import Interface

class Render:

    def __init__(self, pipeline):
        self.__pipeline = pipeline
        self.__active = Window()
        self.__window_stack = []
        self.__event_queue = queues.Queue()

        self.__set_active(self.__active)

    async def execute(self):
        self.__active.render()
        self.__pipeline.execute()
        if Interface.active():
            Interface.schedule(self.execute())

    def submit(self, obj: Primative):
        self.__pipeline.submit(obj)

    async def window_focus(self, window: "Window"):
        self.__window_stack.append(self.__active)
        self.__set_active(window)
        await self.__active.show()

    async def window_pop(self):
        self.__set_active(self.__window_stack.pop())
        await self.__active.show()

    def __set_active(self, window: "Window"):
        self.__active = window
        try:
            while True:
                self.__event_queue.get(False)
        except queues.Empty: pass
        self.__bind_handles()
        self.__pipeline.template = self.__active.template

    def initialize(self):
        self.__pipeline.open()
    def terminate(self):
        self.__pipeline.close()

    async def process(self):
        try:
            while True:
                func, event = self.__event_queue.get(False)
                Interface.schedule(func(event))
        except queues.Empty:
            if Interface.active():
                Interface.schedule(self.process())

    async def __null_binding(self, event):
        return None

    def __bind_handles(self):
        handler = self.__active._event_handler_
        if handler is None:
            for key in range(len(key_names)):
                Key.bind(key, self.__null_binding)

        def wrap(key, handler):
            key = key_names[key]
            async def event(event):
                try:
                    cls = getattr(handler, event)
                    func = getattr(cls, key)
                except AttributeError: return
                cls.window = self.__active
                try:
                    await func(self.__active)
                except Exception as e:
                    print("Event Error", e)

            def submit(ch, event_type):
                self.__event_queue.put((event, event_type))
            return submit

        for key in range(len(key_names)):
            Key.bind(key, wrap(key, handler))