import core
import colorsys
import time

core.asset.Template("True", path="torch/True.template")
core.asset.Template("False", path="torch/False.template")

####MAINWINDOW####
class Mainwindow(core.std.Menu):

    core.hardware.Backlight.fill(225, 225, 225)

    def __init__(self):
        super().__init__(Torch=Torch(), RGB=RGB(), **{"Emergency Light": EmergencyLight()})

######TORCH######
class Torch(core.render.Window):

    def __init__(self):
        self.state = False
        self.template = core.asset.Template(str(self.state))

    def change_state(self):
        self.state = not self.state
        self.template = core.asset.Template(str(self.state))
        if self.state:
            core.hardware.Backlight.fill(255, 255, 255)
            core.hardware.Button.set_led(True)
        else:
            core.hardware.Backlight.fill(0, 0, 0)
            core.hardware.Button.set_led(False)

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Torch

    def press(self):
        self.window.change_state()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Torch

    def press(self):
        core.hardware.Backlight.fill(225, 225, 225)
        core.hardware.Button.set_led(False)
        self.window.finish()

#######RGB#######

class RGB(core.render.Window):

    def __init__(self):
        self.state = (0, 0, 0)
        self.hue = 0

    def bl_set(self):
        R, G, B = colorsys.hsv_to_rgb(self.hue / 100, 1, 1)
        core.hardware.Backlight.fill(int(R*100), int(G*100), int(B*100))

    def increse(self):
        if self.hue < 360:
            self.hue +=1
        else:
            self.hue = 0
        self.bl_set()

    def decrese(self):
        if self.hue > 0:
            self.hue -=1
        else:
            self.hue = 360
        self.bl_set()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = RGB

    def held(self):
        self.window.increse()

    def press(self):
        self.window.increse()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = RGB

    def held(self):
        self.window.decrese()

    def press(self):
        self.window.decrese()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = RGB

    def held(self):
        self.window.finish()

    def press(self):
        core.hardware.Backlight.fill(225, 225, 225)
        self.window.finish()

###EMERGENCYLIGHT###

class EmergencyLight(core.render.Window):

    def __init__(self):
        self.colours = [(255, 0, 0), (255, 255, 255), (0, 0, 255)] # List of colours to cycle through
        self.index = 0

    def render(self):
        self.index = (self.index + 1) % len(self.colours)
        colour = self.colours[self.index]
        core.hardware.Backlight.fill(*colour)
        time.sleep(0.1)

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = EmergencyLight

    def press(self):
        core.hardware.Backlight.fill(225, 225, 225)
        self.window.finish()


main = Mainwindow()
