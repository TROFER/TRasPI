import core
from animatedtext import AnimatedText
from volume import Volume
import pygame

class LocalPlayer(core.render.Window):

    core.asset.Image(
        "play", path=f"{core.sys.PATH}programs/Music Player/asset/play.icon")
    core.asset.Image(
        "pause", path=f"{core.sys.PATH}programs/Music Player/asset/pause.icon")
    core.asset.Image(
        "next", path=f"{core.sys.PATH}programs/Music Player/asset/next.icon")
    core.asset.Image(
        "prev", path=f"{core.sys.PATH}programs/Music Player/asset/prev.icon")

    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.track_number = 0
        self.state = False
        self.centre = [core.asset.Image(
            "pause"), core.asset.Image("play")]
        self.volume = Volume()
        self.trackinfo = AnimatedText((64, 35), self.playlist[self.track_number].description, width=20)
        self.elements = [core.element.Text(core.Vector(64, 5), self.playlist[self.track_number].name),
                    core.element.Line(core.Vector(3, 40),
                                      core.Vector(125, 40), width=2),
                    core.element.Image(core.Vector(44, 53),
                                       core.asset.Image("prev")),
                    core.element.Image(core.Vector(84, 53),
                                       core.asset.Image("next")),
                    core.element.Text(core.Vector(115, 53), self.volume.get()),
                    core.element.Text(core.Vector(15, 53), f"{self.track_number}\{len(self.playlist)}")]

    def render(self):
        self.elements[4].text(self.volume.get())
        core.element.Image(core.Vector(64, 53),
                           self.centre[int(self.state)]).render()
        self.elements[5].text(f"{self.track_number+1}\{len(self.playlist)}")
        for element in self.elements:
            element.render()
        self.trackinfo.render()
        if self.state and time.time() > self.endpoint:
            self.track_number +=1

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



