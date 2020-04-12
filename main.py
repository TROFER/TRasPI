import core

class TWin(core.render.Window):
    def __init__(self):
        super().__init__()
        self.prim = core.element.Text(core.Vector(0, 3), "Hello", justify="L")

    def render(self):
        core.interface.render(self.prim)

class SubWin(core.render.Window):
    def __init__(self):
        super().__init__()
        self.prim = core.element.Text(core.Vector(0, 3), "World", justify="L")

    def render(self):
        core.interface.render(self.prim)

class Handle(core.input.Handler):

    window = TWin

    class press:
        @core.input.event
        async def up(null, window):
            print("Press up on", window)
        @core.input.event
        async def centre(null, window):
            print("Awaiting")
            val = await SubWin()
            print(val)

class Handle(core.input.Handler):

    window = SubWin

    class press:
        @core.input.event
        async def up(null, window):
            print("Press up on", self)
        @core.input.event
        async def centre(null, window):
            print("Returning")
            window.finish("DONE")
            print("Finished")

if __name__ == "__main__":

    app = core.application.Application(TWin())
    core.Interface.run(app)