import core

class Window(core.render.Window):

    def __init__(self):
        super().__init__()
        self.text = core.render.element.Text(core.Vector(64, 32), "MAIN WINDOW")

    def render(self):
        self.text.render()

class SubWindow(core.render.Window):

    def __init__(self):
        super().__init__()
        self.text = core.render.element.Text(core.Vector(64, 32), "SUB WINDOW")

    def render(self):
        self.text.render()

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
            core.render.Render.frame()
    finally:
        core.render.Render().close()

start()


# from core.render import screen
#
# while True:
#     core.render.render()
#     i = input("Input:\n").lower().strip()
#     if i == "a":
#         screen.Screen().test[render.Button.UP.value](
#             core.render.Button.UP.value, "press")
#     elif i == "d":
#         screen.Screen().test[render.Button.DOWN.value](
#             core.render.Button.DOWN.value, "press")
