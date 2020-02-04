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
        "rest", path=f"{core.sys.PATH}programs/Music Player/asset/prev.icon")

    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.track_number = 0
        self.state = False
        self.pause = 0
        self.volume = Volume()
        # ELEMENTS
        self.centre = [core.asset.Image(
            "pause"), core.asset.Image("play")]
        self.trackinfo = AnimatedText(
            (64, 35), self.playlist[self.track_number].description, width=20)
        self.elements = [core.element.Text(core.Vector(64, 5), self.playlist[self.track_number].name),
                         core.element.Line(core.Vector(3, 40),
                                           core.Vector(125, 40), width=2),
                         core.element.Image(core.Vector(44, 53),
                                            core.asset.Image("rest")),
                         core.element.Image(core.Vector(84, 53),
                                            core.asset.Image("next")),
                         core.element.Text(core.Vector(
                             115, 53), self.volume.get()),
                         core.element.Text(core.Vector(15, 53), f"{self.track_number}\{len(self.playlist)}")]
        self.play()

    def render(self):
        # PLAYER
        if self.state:
            if self.endpoint > time.time():
                pygame.mixer.stop()
                self.track_number += 1
                try:
                    self.playlist[self.track_number].play()
                except IndexError:
                    self.stop()
        # END PLAYER
        # ELEMENTS
        self.elements[4].text(self.volume.get())
        core.element.Image(core.Vector(64, 53),
                           self.centre[int(self.state)]).render()
        self.elements[5].text(f"{self.track_number+1}\{len(self.playlist)}")
        for element in self.elements:
            element.render()
        self.trackinfo.render()

    def play(self):
        if not self.state:
            self.endpoint = self.playlist[self.track_number].length(
            ) + (time.time() - self.pause)
            self.state = True
        else:
            self.endpoint = self.playlist[self.track_number].length()
        self.playlist[self.track_number].play()
        self.pause = 0

    def pause(self):
        self.start = time.time()
        self.state = False

    def stop(self):
        self.playlist[self.track_number].stop()

    def toggle(self):
        if self.state:
            self.pause()
        else:
            self.play()

    def skip(self):
        self.stop
        self.track_number += 1
        self.play()


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


class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = LocalPlayer

    def press(self):
        self.window.skip()


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = LocalPlayer

    def press(self):
        self.window.stop()
        self.window.play()


class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = LocalPlayer

    def press(self):
        self.window.volume.increse()


class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = LocalPlayer

    def press(self):
        self.window.volume.decrese()
