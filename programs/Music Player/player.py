import core
from animatedtext import AnimatedText
from volume import Volume
import pygame
import time


def constrain(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


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
        self.state = 0
        self.pausestart = 0
        self.time = time.time()
        self.volume = Volume()
        self.track_pos = 0
        # ELEMENTS
        self.centre = [core.asset.Image(
            "pause"), core.asset.Image("play")]
        self.trackinfo = AnimatedText(
            (64, 35), "Loading", width=20)
        self.elements = [core.element.Text(core.Vector(64, 5), self.playlist[self.track_number].name),
                         core.element.Image(core.Vector(44, 53),
                                            core.asset.Image("rest")),
                         core.element.Image(core.Vector(84, 53),
                                            core.asset.Image("next")),
                         core.element.Text(core.Vector(
                             115, 53), self.volume.get()),
                         core.element.Text(core.Vector(15, 53), f"{self.track_number}\{len(self.playlist)}")]
        self.play()

    def render(self):
        if self.state == 2:
            if self.endpoint < time.time():
                self.stop()
                if self.track_number != len(self.playlist)-1:
                        self.track_number += 1
                        self.play()
            if time.time() - self.time > 1:
                self.track_pos += 1
                self.time = time.time()
                print(self.playlist[self.track_number].length() - self.track_pos)
        core.element.Line(core.Vector(0, 40), core.Vector(constrain(
            self.track_pos, 0, self.playlist[self.track_number].length(), 0, 128), 40), width=2).render()
        self.elements[3].text(self.volume.get())
        core.element.Image(core.Vector(64, 53),
                            self.centre[0 if self.state == 2 else 1]).render()
        self.elements[4].text(
            f"{self.track_number+1}\{len(self.playlist)}")
        self.trackinfo.edit(self.playlist[self.track_number].description)
        self.trackinfo.update()
        for element in self.elements:
            element.render()


    @core.render.Window.focus
    def play(self):
        try:
            if self.state == 0:
                self.endpoint=self.playlist[self.track_number].length(
                ) + time.time()
                self.playlist[self.track_number].play()
            elif self.state == 1:
                self.endpoint=self.playlist[self.track_number].length(
                ) + (time.time() - self.pausestart)
                self.pausestart=0
                self.playlist[self.track_number].unpause()
        except IndexError:
            window=core.std.Info("Queue is empty")
            yield window
        self.state=2

    def pause(self):
        self.start=time.time()
        pygame.mixer.pause()
        self.state=1

    def stop(self):
        pygame.mixer.stop()
        self.state=0

    def toggle(self):
        if self.state == 2:
            self.pause()
        else:
            self.play()

    @core.render.Window.focus
    def skip(self):
        if self.track_number + 1 < len(self.playlist):
            self.stop()
            self.track_number += 1
            self.play()
        else:
            window=core.std.Info("End of Queue")
            yield window


class Handle(core.render.Handler):

    key=core.render.Button.BACK
    window=LocalPlayer

    def press(self):
        self.window.finish()


class Handle(core.render.Handler):

    key=core.render.Button.CENTRE
    window=LocalPlayer

    def press(self):
        self.window.toggle()


class Handle(core.render.Handler):

    key=core.render.Button.RIGHT
    window=LocalPlayer

    def press(self):
        self.window.skip()


class Handle(core.render.Handler):

    key=core.render.Button.LEFT
    window=LocalPlayer

    def press(self):
        self.window.stop()
        self.track_pos=0
        self.window.play()


class Handle(core.render.Handler):

    key=core.render.Button.UP
    window=LocalPlayer

    def press(self):
        self.window.volume.increse()


class Handle(core.render.Handler):

    key=core.render.Button.DOWN
    window=LocalPlayer

    def press(self):
        self.window.volume.decrese()
