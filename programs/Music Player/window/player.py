import datetime
import time
import core
import pygame
from core import Vector, hw
from core.render.element import Image, Line, Rectangle, Text
from core.std import numpad, popup, query
import settings
from .. import app, main, marquee


class Main(core.render.Window):

    def __init__(self, playlist):
        super.__init__()
        self.player = Player(playlist)
        self.elements = [
            Text(Vector(64, 3), ""),
            Text(Vector(3, 3), "", justify='L')
            Line(Vector(0, 8), Vector(128, 8)),
            Text(Vector(3, 10), "", justify='L'),
            marquee.Marquee(Vector(64, 30), "Music Player", width=20),
            Line(Vector(3, 40), Vector(125, 40), width=2),
            Text(Vector(3, 45), "0:00", justify='L'),
            Text(Vector(125, 45), "", justify='R'),
            Image(Vector(64, 55), app.App.asset.pause_icon),
            Image(Vector(40, 55), app.App.asset.rewind_icon),
            Image(Vector(70, 55), app.App.asset.next_icon)]
        self.elements_conditional = [
            Image(Vector(120, 10), app.App.asset.sleep_icon),
            Image(Vector(120, 60), app.App.repeat)]
        self.timeout = 0
        app.App.interval(self.refresh)
        app.App.interval(self.active)
        app.App.interval(self.sleeptimer)
        app.App.interval(self.player.check)
    
    def refresh(self):
        self.elements[0].text = time.strftime("%I:%M%p")
        self.elements[1].text = f"{hw.Battery.percentage}%"
        self.elements[3].text = f"{hw.Audio.current}%"
        self.elements[4].text(self.player.playlist[self.player.track_number].desc)
        self.elements[4].update()
        self.elements[5].pos2 = Vector(app.App.constrain(self.player.endpoint - time.time(), 0, self.player.playlist[self.player.track_number].length, 3, 125) 40)
        self.elements[6].text = datetime.timedelta(seconds=self.player.endpoint - time.time()) 
        self.elements[7].text = datetime.timedelta(seconds=self.player.playlist[self.player.track_number].length) 
        if self.player.state == 1:
            self.elements[8].image = app.App.asset.play_icon
        else:
            self.elements[8].image = app.App.asset.pause_icon

    def render(self):
        for element in self.elements:
            core.interface.render(elements)
        if App.player.sleeptimer != -1:
            core.interface.render(self.elements_conditional[0])
        if App.player.repeat:
            core.interface.render(self.elements_conditional[1])

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
    
    def check(self):
        if time.time > self.endpoint:
            if app.App.player.repeat:
                self.stop()
                self.play()
            else:
                self.skip()