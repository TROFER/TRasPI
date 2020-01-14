import core
import colorsys

core.asset.Image("True", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/True.icon")
core.asset.Image("False", path=f"{core.sys.PATH}/programs/Toolbox/Flashlight/False.icon")

class Mainwindow(core.render.Window):

    def __init__(self):
        self.state, self.brightneess = True, 100
        self.text = core.element.Text(core.Vector(64, 50), "Press Back to Return")

    def inc_brightness(self):
        if self.brightness < 100:
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
            core.hardware.Backlight.Fill(int(2.55 * self.brightness), int(2.55 * self.brightness), int(2.55 * self.brightness))
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

main = Mainwindow()


'''R, G, B = colorsys.hsv_to_rgb(self.hue / 100, 1, 1)
core.hardware.Backlight.fill(int(R*100), int(G*100), int(B*100))'''

'''self.index = (self.index + 1) % len(self.colours)
colour = self.colours[self.index]
core.hardware.Backlight.fill(*colour)
time.sleep(0.1)'''
