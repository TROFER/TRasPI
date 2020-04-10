import core

class TWin(core.render.Window):
    def __init__(self):
        self.prim = core.render.primative.Test("Main")

    def render(self):
        core.Application().render.submit(self.prim)

class SubWin(core.render.Window):
    def __init__(self):
        self.prim = core.render.primative.Test("Sub")

    def render(self):
        core.Application().render.submit(self.prim)

class Handle(core.input.Handler):

    window = TWin

    class press:

        async def up(self):
            print("Press up on", self.window)

        async def centre(self):
            print("Awaiting")
            val = await SubWin()
            print(val)

class Handle(core.input.Handler):

    window = SubWin

    class press:

        async def up(self):
            print("Press up on", self.window)

        async def centre(self):
            print("Returning")
            self.window.finish("DONE")

if __name__ == "__main__":

    app = core.application.Application(TWin())

    core.Interface.run(app)
