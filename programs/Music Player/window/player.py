import time
import core
import pygame
from .. import main
import settings
from core import Vector
from core import hw
from core.render.element import Line, Text, Rectangle, Image
from core.std import popup, numpad, query


class Main(core.render.Window):

    def __init__(self, playlist):
        super.__init__()
        self.player = Player(playlist)
        self.elements = [
            Text(Vector(64, 3), f"{playlist.name} - Music Player"),
            Line(Vector(0, 8), Vector(128, 8)),
            Image(Vector)
        ]
        self.timeout = 0
        App.interval(self.active)
        App.interval(self.sleeptimer)

    def render(self):
        for element in self.elements:
            core.interface.render(elements)

    def active(self):
        if self.timeout >= App.const.screen_timeout:
            hw.Backlight.fill([App.const.colour, 1, 0.3])
            self.timeout = -1
        elif self.timeout == -1:
            pass
        else:
            self.timeout += 1

    def sleeptimer(self):
        if App.player.sleeptimer == 0:
            self.player.stop()
            hw.Power.halt()
        if App.player.sleeptimer != -1:
            App.player.sleeptimer -= 1


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.skip()

        async def left(null, window: Main):
            window.stop()

        async def centre(null, window: Main):
            if window.state == 2:
                window.pause()
            else:
                window.play()

        async def up(null window: Main):
            await settings.Main()


class Player:

    def __init__(self, playlist):
        self.playlist = playlist
        self.track_number = 0
        self.state = 0  # State 0 = Stopped, State 1 = Paused, State 2 = Playing
        self.pausestart = 0

    def play(self):
        if self.state == 0:
            try:
                self.playlist[self.track_number].play()
                self.endpoint = self.playlist[self.track_number].length + time.time()
            except FileNotFoundError:
                await popup.Error("File not found")
                return
        elif self.state == 1:
            self.endpoint += time.time() - self.pausestart
            self.pausestart = 0
            pygame.mixer.music.unpause()
        self.state = 2

    def pause(self):
        self.pausestart = time.time()
        pygame.mixer.music.pause()
        self.state = 1

    def stop(self):
        pygame.mixer.music.stop()
        self.state = 0
        self.track_number = 0

    def skip(self):
        if self.track_number != len(self.playlist) - 1:
            self.stop()
            self.track_number += 1
            self.play()
        else:
            await popup.Info("End of queue")

