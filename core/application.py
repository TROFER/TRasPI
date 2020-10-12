import threading
import traceback

from .sys import log
from .driver.pipeline.render import Render as Pipeline
from .render.render import Render
from .sys.load import load as Load
from .asset import base as AssetBase

from .sys.program import Program

from .interface import Interface

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
        self.applications = set()

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
        await self.__close_program(self.__home)

    async def kill_program(self, program: Program):
        if program is self.__current_app:
            await self.home()
        await self.__close_program(program)

    async def home(self, value: int=2):
        if self.__current_app is self.__home:
            return self.render.enable()
        log.core.info("Return to Home %s", self.__home)
        current = self.__current_app
        await self.__change_program(self.__home)
        if value == -1:
            await self.__close_program(current)

    async def program(self, program: Program):
        try:
            log.core.info("Switching %s", program)
            if program not in self.applications:
                await self.__start_program(program)
            await self.__change_program(program)
        except Exception as e:
            # print("Program:", "".join(traceback.format_exception(e, e, e.__traceback__)))
            log.core.error("%s - %s: %s", program, type(e).__name__, e)
            log.traceback.error("Failed to Switch Program: %s", program, exc_info=e)
            await self.home()

    async def __start_program(self, program: Program):
        self.render.disable()
        Load.reload(program)
        await program.open()
        self.applications.add(program)

    async def __change_program(self, program: Program):
        self.render.disable()
        await self.render.switch_start()
        await self.__current_app.hide()
        AssetBase.search(self.__current_app._file+"resource/{name}/", False)
        self.__current_app.window_stack, self.__current_app.window_active = self.render.change_stack(program.window_stack, program.window_active)
        self.__current_app = program
        log._active_program = self.__current_app.application.name
        AssetBase.search(self.__current_app._file+"resource/{name}/")
        await self.__current_app.show()
        await self.render.switch_end()
        self.render.enable()

    async def __close_program(self, program: Program):
        await program.hide()
        await program.close()
        try:
            self.applications.discard(program)
            Load.close(program)
        except ValueError:
            pass

    async def main(self):
        await self.__current_app.main()

    async def run(self):
        Interface.schedule(self.render.execute())
        Interface.schedule(self.render.process())
        await self.__current_app.open()
        self.render.change_stack(self.__current_app.window_stack, self.__current_app.window_active)
        await self.__current_app.show()
        Interface.schedule(self.__current_app.window_active.show())
        self.render.enable()

    def deltatime(self) -> float:
        return self.render.deltatime

def main(application: Application):
    application.main()

def app() -> Application:
    return _Active.active(Application)
