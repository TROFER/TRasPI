import core
import colorsys
import time

True_icon = core.asset.Image("True", path="Torch/True.icon")
False_icon = core.asset.Image("False", path="Torch/False.icon")
RGB_icon = core.asset.Image("RGB", path="Torch/RGB.icon")

####MAINWINDOW####
class Mainwindow(core.std.MenuSingle):

    def __init__(self):
        Torch, RGB, EMG = Torch(), RGB(), EmergencyLight()
        yield Torch
        core.hardware.Backlight.fill(0, 225, 225)
        super().__init__(Torch, RGB, EMG)

######TORCH######
class Torch(core.render.Window):

    def __init__(self):
        self.state = False
        self.brightness = 255
        self.template = core.asset.Template(str(self.state))

    def change_state(self):
        self.state = not self.state
        self.icon = core.element.Image(core.Vector(64, 32), core.asset.Image(self.state))
        if self.state:
            core.hardware.Backlight.fill(self.brightness, self.brightness, self.brightness)
            core.hardware.Button.led(True)
        else:
            core.hardware.Backlight.fill(0, 0, 0)
            core.hardware.Button.led(False)

    def increse(self):
        if self.brightness < 225:
            self.brightness += 1

    def decrese(self):
        if self.brightness > 0:
            self.brightness -= 1

    def render(self):
        self.icon.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Torch

    def press(self):
        self.window.change_state()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Torch

    def press(self):
        core.hardware.Button.led(False)
        self.window.finish()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Torch

    def press(self):
        self.window.finish()

#######RGB#######

class RGB(core.render.Window):

    def __init__(self):
        self.state = (0, 0, 0)
        self.hue = 0
        self.icon = core.element.Image(core.Vector(64, 32), core.asset.Image("RGB"))

    def apply(self):
        R, G, B = colorsys.hsv_to_rgb(self.hue / 100, 1, 1)
        core.hardware.Backlight.fill(int(R*100), int(G*100), int(B*100))

    def increse(self):
        if self.hue < 360:
            self.hue +=1
        else:
            self.hue = 0
        self.apply()

    def decrese(self):
        if self.hue > 0:
            self.hue -=1
        else:
            self.hue = 360
        self.apply()

    def render(self):
        self.icon.render()

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
        core.hardware.Backlight.fill(0, 225, 225)
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
        core.hardware.Backlight.fill(0, 225, 225)
        self.window.finish()


main = Mainwindow()
