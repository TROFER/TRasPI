import core
import time

class Window(core.render.Window):

    def __init__(self):
        super().__init__()
        self.text = core.render.element.Text(core.Vector(64, 32), "MAIN WINDOW")

    def render(self):
        self.text.render()

class SubWindow(core.render.Window):

    def __init__(self):
        super().__init__()
        self.text = [
            core.render.element.Text(core.Vector(64, 32), "ABCDEFGHIJKLM"),
            core.render.element.Text(core.Vector(64, 32), "NOPQRSTUVWXYZ"),
        ]
        self.index = 0

    def render(self):
        self.text[self.index].render()
        self.index = (self.index + 1) % len(self.text)

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Window

    def press(self):
        print("MAIN GOT PRESS EVENT ON", self.window)
        test = yield SubWindow()
        print(test)

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = SubWindow

    def press(self):
        print("SUB GOT PRESS EVENT ON", self.window)
        self.window.finish("XD")

w = Window()
w.show()

def start():
    execute = True
    core.render.Render().start()
    try:
        while execute:
            core.render.render()
            core.render.Render().frame()
    except BaseException:
        print("Exiting")
    finally:
        core.render.Render().close()

start()
