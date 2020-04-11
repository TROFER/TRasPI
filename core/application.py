import threading
from core.driver.pipeline.render import Render as Pipeline
from core.render.render import Render
from core.render.window import Window

from core.interface import Interface

class _Active(type):

    __instance = None
    def __call__(cls, *args, new=False, **kwargs):
        if new or cls.__instance is None:
            return super().__call__(*args, **kwargs)
        return cls.__instance

    def activate(cls, obj):
        cls.__instance = obj

    def active(cls):
        return cls.__instance

class Application(metaclass=_Active):

    def __init__(self, window: Window):
        self.running = False
        self.render = Render(Pipeline())
        self.__window = window

    def initialize(self):
        self.__class__.activate(self)
        self.running = True
        self.render.initialize()

    def terminate(self):
        self.running = False
        self.render.terminate()
        self.__class__.activate(None)

    async def main(self):
        Interface.schedule(self.render.execute())
        Interface.schedule(self.render.process())
        Interface.schedule(self.__window.focus())

def main(application: Application):
    application.main()

def app() -> Application:
    return _Active.active(Application)
