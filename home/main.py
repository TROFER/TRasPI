import core
import home
import time

class Mainwindow(core.render.Window):

    template = core.asset.Template("std::window", path="window.template")

    def __init__(self):
        self.index = 0
        self.functions = {0: home.ProgramMenu(), 1: home.SettingsWindow(), 2: home.PowerMenu()}
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        self.title1 = core.element.Text(core.Vector(3, 5), "TRasPi OS", justify="L")
        self.buttons = [core.element.TextBox(core.Vector(64, 18), "Run Program"),
        core.element.TextBox(core.Vector(64, 30), "System Settings"),
        core.element.TextBox(core.Vector(64, 42), "Power Options")]
        self.title2 = core.element.Text(core.Vector(126, 5), "TIME", justify="R")
        self.clock(), self.update_arrow()

    def clock(self):
        self.title2.text(time.strftime('%I:%M%p'))

    def update_arrow(self):
        self.left_arrow = core.element.Text(core.Vector(self.buttons[self.index].pos_abs[0] - 2, self.buttons[self.index].pos[1]), ">", justify="R")
        self.right_arrow = core.element.Text(core.Vector(128 - self.buttons[self.index].pos_abs[0] + 2, self.buttons[self.index].pos[1]), "<", justify="L")

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
