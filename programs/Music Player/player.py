import core
from animatedtext import AnimatedText
from volume import Volume

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
        self.centre = [core.asset.Image(
            "stop"), core.asset.Image("play")]
        self.volume = Volume()
        self.trackinfo = AnimatedText((65, 35), track.description)
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
        if self.state:
            self.state = False
            pygame.mixer.pause()
            self.start = time.time()
        if not self.state:
            self.state = True
            pygame.mixer.play()
            self.endpoint += time.time() - self.start
            self.start = 0


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



