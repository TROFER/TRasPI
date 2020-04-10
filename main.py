import core

class TWin(core.render.Window):
    def __init__(self):
        self.prim = core.element.Text(core.Vector(0, 5), "Hello", justify="L")

    def render(self):
        core.interface.render(self.prim)

class SubWin(core.render.Window):
    def __init__(self):
        self.prim = core.element.Text(core.Vector(0, 5), "World", justify="L")

    def render(self):
        core.interface.render(self.prim)

class Handle(core.input.Handler):

    window = TWin

    class press:

        @core.input.event
        async def up(self):
            print("Press up on", self.window)

        @core.input.event
        async def centre(self):
            print("Awaiting")
            val = await SubWin()
            print(val)

class Handle(core.input.Handler):

    window = SubWin

    class press:

        @core.input.event
        async def up(self):
            print("Press up on", self)

        @core.input.event
        async def centre(self):
            print("Returning")
            self.finish("DONE")

if __name__ == "__main__":

    app = core.application.Application(TWin())

    core.Interface.run(app)
