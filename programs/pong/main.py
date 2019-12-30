import core
import time

title = core.asset.Image("title", f"{core.sys.PATH}programs/pong/title.asset")

class TitleScreen(core.render.Window):

    def __init__(self):
        self.time = time.time()
        self.index = 0
        self.title = core.element.Image(core.Vector(64, 16), core.asset.Image("title"))
        self.bttns = [core.element.TextBox(core.Vector(64, 25), "Singleplayer"),
            core.element.TextBox(core.Vector(64, 35), "Leaderboards"),
            core.element.TextBox(core.Vector(64, 25), "Quit Game")]
        self.left_arrow = core.element.Text(core.Vector(self.bttns[self.index].pos_abs[0] - 2, self.bttns[self.index].pos[1]), ">", justify="R")
        self.right_arrow = core.element.Text(core.Vector(128 - self.bttns[self.index].pos_abs[0] + 2, self.bttns[self.index].pos[1]), "<", justify="L")

    
    def select(self):
        pass

    def down(self):
        pass

    def up(self):
        pass

    def render(self):
        if time.time() - self.time > 1.5:
            self.title.pos[1] += 1
            self.title.render()
            self.title.pos[1] -= 1
        else:
            self.title.render()
        for bttn in self.bttns:
            bttn.render()
        self.left_arrow.render(), self.right_arrow.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTER
    window = TitleScreen

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = TitleScreen

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = TitleScreen

    def press(self):
        self.window.down()

main = TitleScreen()
