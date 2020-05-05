import threading
import traceback

from core.driver.pipeline.render import Render as Pipeline
from core.render.render import Render
from core.sys.load import load as Load

from core.sys.program import Program

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

    def __init__(self, app: Program):
        self.running = threading.Event()
        self.render = Render(Pipeline(), self.home)
        self.__home = app
        self.__current_app = self.__home
        self.applications = {self.__current_app}

    def initialize(self):
        self.__class__.activate(self)
        self.running.set()
        self.render.initialize()

    def terminate(self):
        self.running.clear()
        self.render.terminate()
        self.__class__.activate(None)

    async def close_all(self):
        await self.home(-1)
        for app in tuple(self.applications):
            await self.__close_program(app)

    async def home(self, value: int):
        if self.__current_app is self.__home:
            return # Do the funky

        current = self.__current_app
        await self.__change_program(self.__home)
        if value == -1:
            await self.__close_program(current)

    async def program(self, program: Program):
        if program not in self.applications:
            await self.__start_program(program)
        await self.__change_program(program)

    async def __start_program(self, program: Program):
        self.render.disable()
        self.applications.add(program)
        await program.open()

    async def __change_program(self, program: Program):
        self.render.disable()
        self.__current_app.window_stack, self.__current_app.window_active = self.render.change_stack(program.window_stack, program.window_active)
        await self.__current_app.hide()
        self.__current_app = program
        await self.__current_app.show()
        self.render.enable()

    async def __close_program(self, program: Program):
        await program.hide()
        await program.close()
        self.applications.discard(program)
        Load.close(program)

    async def main(self):
        await self.__current_app.main()

    async def run(self):
        try:
            Interface.schedule(self.render.execute())
            Interface.schedule(self.render.process())
            await self.__current_app.open()
            self.render.change_stack(self.__current_app.window_stack, self.__current_app.window_active)
            await self.__current_app.show()
            Interface.schedule(self.__current_app.window_active.show())
            self.render.enable()
        except Exception as e:
            print(traceback.print_exception(e, e, e.__traceback__))
            raise

def main(application: Application):
    application.main()

def app() -> Application:
    return _Active.active(Application)
