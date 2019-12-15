import core
import colorsys
import time
####MAINWINDOW####
class Mainwindow(core.std.Menu):

    def __init__(self):
        super().__init__(Torch=Torch(), RGB=RGB(), **{"Emergency Light": EmergencyLight()})

######TORCH######
class Torch(core.render.Window):

    def __init__(self):
        self.state = False
        self.template = f"{core.sys.PATH}programs/torch/{self.state}.template"

    def change_state(self):
        self.state = not self.state
        self.template = f"{core.sys.PATH}programs/torch/{self.state}.template"
        if self.state:
            core.hardware.backlight.fill(225, 225, 225)
        else:
            core.hardware.backlight.fill(0, 0, 0)

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Torch

    def press(self):
        self.window.change_state()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Torch

    def press(self):
        self.window.finish()

#######RGB#######

class RGB(core.render.Window):

    def __init__(self):
        self.state = (0, 0, 0)
        self.hue = 0

    def bl_set(self):
        core.hardware.backlight.fill(*colorsys.hsv_to_rgb(self.hue, 100, 100))

    def increse(self):
        if self.hue < 360:
            self.hue +=1
        else:
            self.hue = 0
        bl_set()

    def decrese(self):
        def increse(self):
            if self.hue > 0:
                self.hue -=1
            else:
                self.hue = 360
        bl_set()

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
        self.window.increse()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = RGB

    def held(self):
        self.window.finish()

    def press(self):
        self.window.finish()

###EMERGENCYLIGHT###

class EmergencyLight(core.render.Window):

    def __init__(self):
        self.colours = [(255, 0, 0), (255, 255, 255), (0, 0, 255)] # List of colours to cycle through
        self.index = 0

    def render(self):
        self.index = (self.index + 1) % len(self.colours)
        colour = self.colours[self.index]
        core.render.backlight.fill(*colour)
        time.sleep(0.1)

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = RGB

    def press(self):
        self.window.finish()






main = Mainwindow()
