import core
import time

class Mainwindow(core.render.Window):

    def __init__(self):
        # Elements
        self.template = f"{core.sys.PATH}core/resource/template/home.template"
        self.title1 = core.render.element.Text(core.Vector(3, 5), "TRasPi OS", justify="L")
        self.title2 = core.render.element.Text(core.Vector(126, 5), time.strftime('%I:%M%p'), justify="R")
        self.bttn1 = core.render.element.TextBox(core.Vector(64, 18), "Run Program")
        self.bttn2 = core.render.element.TextBox(core.Vector(64, 30), "Load Program")
        self.bttn3 = core.render.element.TextBox(core.Vector(64, 42), "System Settings")
        self.bttn4 = core.render.element.TextBox(core.Vector(64, 54), "Power Options")
        # Variables
        self.index = 0
        self.functions = {0: "core.loader.run", 1: "core.render.load", 2: "core.sys.configurator", 3: "core.sys.powermenu"} #Needs to be ajusted if name changes
        # Misc
        core.hardware.Backlight.gradient((240, 205, 205, 240))

    def render(self):
        self.title1.render(), self.title2.render()
        self.bttn1.render(), self.bttn2.render(), self.bttn3.render(), self.bttn4.render()

    def up(self):
        if self.index > 0:
            self.index -=1 #Needs to reposiiton

    def down(self):
        if self.index < len(self.functions):
            self.index +=1

    def select(self):
        pass


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
