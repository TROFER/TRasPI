import core
import json

class Mainwindow(core.render.Window):

    def __init__(self):
        self.images = json.load(f"{core.sys.PATH}programs/asset inspector/register.json")
        self.index = 0
        self.max = len(self.images)

    def render(self):
        self.template = self.images[self.index]

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Mainwindow

    def press(self):
        if self.index+1 < self.max:
            self.window.next()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Mainwindow

    def press(self):
        if self.index-1 > 0:
            self.window.previous()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Mainwindow

    def press(self):
        self.window.finish()

main = Mainwindow()
