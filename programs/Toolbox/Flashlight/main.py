import core
import colorsys
import time

core.asset.Image("True", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/assets/True.icon")
core.asset.Image("False", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/assets/False.icon")
core.asset.Image("RGB", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/assets/rgb.icon")
core.asset.Image("EMG", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/assets/emg.icon")

class Flashlight(core.render.Window):

    def __init__(self):
        self.state, self.brightness, self.step = True, 100, [25, 50, 75, 100]
        self.text = core.element.Text(core.Vector(64, 50), "Press Back to exit")

    def inc_brightness(self):
        if self.brightness < 3:
            self.brightness += 1
            self.refresh()

    def dec_brightness(self):
        if self.brightness > 0:
            self.brightness -= 1
            self.refresh()

    def toggle(self):
        self.state != self.state
        self.refresh()

    def refresh(self):
        if self.state:
            core.hardware.Backlight.Fill(int(2.55 * self.step[self.brightness]), int(2.55 * self.step[self.brightness]),
             int(2.55 * self.step[self.brightness]))
        else:
            core.hardware.Backlight.Fill(0, 0, 0)
        core.hardware.Button.led(self.state)

    def render(self):
        self.image = core.element.Image(core.Vector(64, 32), core.asset.Image(self.state))
        self.text.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Mainwindow

    def press(self):
        self.window.toggle()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Mainwindow

    def press(self):
        core.hardware.Button.led(False)
        self.window.finish()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Mainwindow

    def press(self):
        self.window.inc_brightness()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Mainwindow

    def press(self):
        self.window.dec_brightness()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Mainwindow

    def press(self):
        core.hardware.Button.led(False)
        RGB = RGB()
        res = yield RGB
        if res == 0:
            self.window.finish()

class RGB(core.render.Window):

    def __init__(self):
        self.hue = 0
        self.icon = core.element.Image(core.Vector(64, 32), core.asset.Image("RGB"))
        self.text = core.element.Text(core.Vector(64, 50), "Press Back to exit")
        self.label_hue = core.element.Text(core.Vector(64, 10), self.hue)

    def refresh(self):
        R, G, B = colorsys.hsv_to_rgb(self.hue / 100, 1, 1)
        core.hardware.Backlight.fill(int(R*100), int(G*100), int(B*100))

    def inc_hue(self):
        if self.hue < 360:
            self.hue += 1
            self.refresh()

    def dec_hue(self):
        if self.hue > 0:
            self.hue -=1
            self.refresh()

    def render(self):
        self.label_hue = core.element.Text(core.Vector(64, 10), self.hue)
        self.icon.render()
        self.text.render()
        self.label_hue.render()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Mainwindow

    def press(self):
        EMG = EMG()
        res = yield EMG
        if res == 0:
            self.window.finish(0)

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Mainwindow

    def press(self):
        self.window.finish(1)

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Mainwindow

    def press(self):
        self.window.finish(0)

class EMG(core.render.Window):

    def __init__(self):
        self.colours = [(255, 0, 0), (0, 0, 0), (0, 0, 255)]
        self.index = 0
        self.icon = core.element.Image(core.Vector(64, 32), core.asset.Image("EMG"))

    def render(self):
        self.icon.render()
        core.hardware.Backlight.Fill(*self.colours[self.index])
        self.index += 1
        time.sleep(1)

    class Handle(core.render.Handler):

        key = core.render.Button.BACK
        window = Mainwindow

        def press(self):
            self.window.finish(0)

    class Handle(core.render.Handler):

        key = core.render.Button.LEFT
        window = Mainwindow

        def press(self):
            self.window.finish(1)

main = Mainwindow()
