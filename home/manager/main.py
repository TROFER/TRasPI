import core

class App(core.type.Application):
    name = "Task Manager"

class TaskManager(core.render.Window):

    def __init__(self):
        super().__init__()
        self.index = 0
        self.active = []

        self.selected = core.render.element.Text(core.Vector(core.sys.const.width // 2, core.sys.const.height // 2), "Active")

    async def show(self):
        self.index = 0
        self.active = list(core.interface.application().applications)
        core.log.debug("Active Programs: %d", len(self.active))
        self.move(0)

    def render(self):
        core.interface.render(self.selected)

    def move(self, index: int):
        self.index = (self.index + index) % len(self.active)
        self.selected.text = self.active[self.index].application.name

    async def kill(self, program: core.application.Program):
        if program in core.interface.application().applications:
            await self._kill(program)

    async def _kill(self, program: core.application.Program):
        await core.interface.application().kill_program(program)
        await self.show()
        self.move(0)

class Handler(core.input.Handler):
    window = TaskManager
    class press:
        async def left(null, window: TaskManager):
            window.move(-1)
        async def right(null, window: TaskManager):
            window.move(1)
        async def down(null, window: TaskManager):
            p = window.active[window.index]
            if await core.std.Query(f"{p.application.name}", "Kill Application"):
                await window.kill(p)
        async def centre(null, window: TaskManager):
            core.interface.program(window.active[window.index])

App.window = TaskManager
main = App