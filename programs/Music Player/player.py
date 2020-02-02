import core
from animatedtext import AnimatedText

class LocalPlayer(core.render.Window):

    core.asset.Image(
        "play", path=f"{core.sys.PATH}programs/Music Player/asset/play.icon")
    core.asset.Image(
        "pause", path=f"{core.sys.PATH}programs/Music Player/asset/pause.icon")
    core.asset.Image(
        "next", path=f"{core.sys.PATH}programs/Music Player/asset/next.icon")
    core.asset.Image(
        "prev", path=f"{core.sys.PATH}programs/Music Player/asset/prev.icon")

    def __init__(self, track):
        self.state = False
        self.element_control_centre = [core.asset.Image(
            "stop"), core.asset.Image("play")]
        self.stext = AnimatedText((64, 45), track.description)
        elements = [core.element.Text(core.Vector(64, 3), track.name),
                    core.element.Line(core.Vector(3, 47),
                                      core.Vector(125, 47), width=2),
                    core.element.Image(core.Vector(63, 55),
                                       self.element_control_centre[int(self.state)]),
                    core.element.Image(core.Vector(25, 50),
                                       core.asset.Image("prev")),
                    core.element.Image(core.Vector(75, 50),
                                       core.asset.Image("next")),
                    core.element.Text(core.Vector(102, 57), self.volume.get())]

    def render(self):
        for element in self.elements:
            element.render()
        self.stext.render()

    def toggle(self):
        self.state != self.state


class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = LocalPlayer

    def press(self):
        self.window.finish()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = LocalPlayer

    def press(self):
        self.window.toggle()


class Volume:

    def __init__(self, step=5):
        self.volume = 75
        self.step = step
        self.set()

    def set(self):
        os.system(f"amixer set Master {self.volume}%")

    def get(self):
        return "{self.volume}%"

    def decrese(self):
        self.volume -= self.step
        self.set()

    def increse(self):
        self.volume += self.step
        self.step()
