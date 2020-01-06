import core

class MainWindow(core.render.Window):

    template = core.asset.Template("std::window")

    def __init__(self):
        core.hardware.Backlight.fill(255, 255, 255)
        self.contrast = 20
        self.title = core.element.Text(core.Vector(3, 5), "Ajust Contrast", justify="L")
        self.message1 = core.element.Text(core.Vector(64, 15), "UP -Increse Contrast")
        self.message2 = core.element.Text(core.Vector(64, 25), "DOWN -Decrese Contrast")

    def render(self):
        self.title.render()
        self.message1.render()
        self.message2.render()

    def up(self):
        if self.contrast < 63:
            self.contrast += 1
            core.render.Renderer.pause(empty=True)
            core.hardware.Display.contrast(self.contrast)
            core.render.renderer.resume()

    def down(self):
        if self.contrast > 0:
            self.contrast -= 1
            core.render.Renderer.pause(empty=True)
            core.hardware.Display.contrast(self.contrast)
            core.render.renderer.resume()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = MainWindow

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = MainWindow

    def press(self):
        self.window.down()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = MainWindow

    def press(self):
        self.window.finish()

main = MainWindow()
