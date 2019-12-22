import core
import time

class Mainwindow(core.render.Window):

    template = core.asset.Template("home", path="window.template")

    def __init__(self):
        self.index = 0
        self.functions = {0: core.system.ProgramMenu(), 1: core.std.Error("Not Ready"), 2: core.system.PowerMenu()}
        core.hardware.Backlight.gradient((240, 180, 240, 180, 240))
        self.title1 = core.render.element.Text(core.Vector(3, 5), "TRasPi OS", justify="L")
        self.buttons = [core.render.element.TextBox(core.Vector(64, 18), "Run Program"),
        core.render.element.TextBox(core.Vector(64, 30), "System Settings"),
        core.render.element.TextBox(core.Vector(64, 42), "Power Options")]
        self.clock()

    def clock(self):
        self.title2 = core.render.element.Text(core.Vector(126, 5), time.strftime('%I:%M%p'), justify="R")

    def update_arrow(self):
        self.left_arrow = core.render.element.Text(core.Vector(self.buttons[self.index].position[0] - 2, self.buttons[self.index].pos[1]), ">", justify="R")
        self.right_arrow = core.render.element.Text(core.Vector(128 - self.buttons[self.index].position[0] + 2, self.buttons[self.index].pos[1]), "<", justify="L")

    def render(self):
        self.clock()
        self.title1.render(), self.title2.render()
        for button in self.buttons:
            button.render()
        self.left_arrow.render(), self.right_arrow.render()

    def up(self):
        if self.index > 0:
            self.index -=1
            self.update_arrow()

    def down(self):
        if self.index < len(self.functions)-1:
            self.index +=1
            self.update_arrow()

    @core.render.Window.focus
    def select(self):
        command =  self.functions[self.index]
        res = yield command

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Mainwindow

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Mainwindow

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Mainwindow

    def press(self):
        self.window.down()

main = Mainwindow()
main.show()
core.render.loop()
