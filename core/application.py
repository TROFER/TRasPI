from core.driver.pipeline.render import Render as Pipeline
from core.render.render import Render

from core.type.application import Application as TApplication
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

    def __init__(self, app: TApplication):
        self.running = False
        self.render = Render(Pipeline(), self.home)
        self.__home = app._program
        self.__current_app = self.__home
        self.applications = {}

    def initialize(self):
        self.__class__.activate(self)
        self.running = True
        self.render.initialize()

    def terminate(self):
        self.running = False
        self.render.terminate()
        self.__class__.activate(None)

    async def home(self):
        if self.__current_app is self.__home:
            # Do the funky
            return

        self.__change_program(self.__home)

    async def __change_program(self, program: Program):
        self.__current_app.window_stack, self.__current_app.window_active = self.render.change_stack(program.window_stack, program.window_active)
        await self.__current_app.hide()
        self.__current_app = program
        await self.__current_app.show()

    async def main(self):
        await self.__current_app.main()

    async def run(self):
        try:
            Interface.schedule(self.render.execute())
            Interface.schedule(self.render.process())
            await self.__current_app.open()
            self.render.change_stack(self.__current_app.window_stack, self.__current_app.window_active, enable=False)
            await self.__current_app.show()
            Interface.schedule(self.__home.application.window.show())
            self.render.enable()
            # Interface.schedule(self.__home.application.window.focus())
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            raise

def main(application: Application):
    application.main()

def app() -> Application:
    return _Active.active(Application)
