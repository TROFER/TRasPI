import queue as queues

from core.render.primative import Primative

_keys = ["up", "down", "back", "left", "centre", "right"]

class Render:

    def __init__(self, pipeline, window: "Window"):
        self.__pipeline = pipeline
        self.__active = window
        self.__window_stack = []
        self.__event_queue = queues.Queue()

    def execute(self):
        self.__active.render()
        self.__pipeline.execute()

    def submit(self, obj: Primative):
        self.__pipeline.submit(obj)

    async def window_focus(self, window: "Window"):
        self.__window_stack.append(self.__active)
        await self.__set_active(window)

    async def window_pop(self):
        await self.__set_active(self.__window_stack.pop())

    async def __set_active(self, window: "Window"):
        self.__active = window
        try:
            while True:
                self.__event_queue.get(False)
        except queues.Empty: pass
        self.__bind_handles()
        self.__pipeline.template = self.__active.template
        await self.__active.show()

    def initialize(self):
        self.__pipeline.open()
    def terminate(self):
        self.__pipeline.close()

    async def process(self):
        try:
            while True:
                func, event = self.__event_queue.get(False)
                await func(event)
        except queues.Empty:    return

    def __bind_handles(self):
        handler = self.__active._event_handler_
        if handler is None:
            pass

        def wrap(key, handler):
            key = _keys[key]
            def event(event):
                try:
                    cls = getattr(handler, event)
                    func = getattr(cls, key)
                except AttributeError: return
                cls.window = self.__active
                try:
                    return func()
                except Exception as e:
                    print("Event Error", e)

            def submit(ch, event_type):
                self.__event_queue.put((event, event_type))
            return submit

        for key in range(len(_keys)):
            print("Bound Key", key, wrap(key, handler))
            # Touch.bind(key, wrap(key, handler))