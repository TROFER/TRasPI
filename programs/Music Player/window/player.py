import asyncio
import time

import core
from app import App
from core import Vector
from core.render.element import Image, Line, Marquee, Text
from core.std import menu, numpad, query

import player


class Base(core.render.Window):

    PLAYER = player.main

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.c = self.db.cursor()
        self._sleeptimer = None
        self.playerstate = True
        # Elements
        self.title = Text(Vector(64, 5))
        self.battery_icon = Image(
            Vector(1, 3), App.asset.battery_icon, just_w='L')
        self.battery_percentage = Text(Vector(13, 5), justify='L')
        self.title_line = Line(Vector(0, 9), Vector(128, 9))
        self.volume_percentage = Text(Vector(127, 14), justify='R')
        self.sleep_icon = Image(
            Vector(1, 11), App.asset.sleep_icon, just_w='L')
        self.marquee = Marquee(Vector(64, 32), width=20, small=False)
        self.elements = {self.title, self.battery_icon, self.battery_percentage,
                         self.title_line, self.volume_percentage, self.marquee}
        # Scheduling
        self.timeout = core.Interface.loop.create_future()
        App.interval(self.refresh)

    def refresh(self):
        self.title.text = time.strftime("%I:%M%p")
        self.battery_percentage.text = f"{core.hw.Battery.percentage()}%"
        self.volume_percentage.text = f"{core.hw.Audio.current()}%"

    async def show(self):
        self.powersaving()
        self.refresh()

    def render(self):
        if self._sleeptimer is not None:
            core.interface.render(self.sleep_icon)
        for element in self.elements:
            core.Interface.render(element)

    async def _powersaving(self, future):
        if future.done():
            core.hw.Backlight.fill(core.sys.var.colour)
            self.marquee.play()
        await asyncio.sleep(App.const.screen_timeout)
        core.hw.Backlight.fill(core.sys.var.colour)
        self.marquee.pause()

    def powersaving(self, cancel=False):
        self.timeout = core.Interface.schedule(self._powersaving(self.timeout))
        if cancel:
            self.timeout.cancel()

    async def sleeptimer(self, time: int):
        await asyncio.sleep(time)
        core.hw.Power.halt()

    def _finish(self):
        self.powersaving(cancel=True)
        if self._sleeptimer is not None:
            self._sleeptimer.cancel()
        self.finish()


class Main(Base):

    def __init__(self, db, playlist):
        super().__init__(db)
        self.tracknumber = 0
        self._repeat_flag = False
        self.playlist = self._fill(playlist)
        # Elements
        self.progress_bar = Line(Vector(3, 40), Vector(3, 40), width=2)
        self.timestamp_current = Text(Vector(3, 46), justify='L')
        self.timestamp_total = Text(Vector(127, 46), justify='R')
        self.pause_icon = Image(
            Vector(64, 53), App.asset.pause_icon, just_h='C')
        self.rewind_icon = Image(
            Vector(52, 53), App.asset.rewind_icon, just_h='C', just_w='R')
        self.next_icon = Image(
            Vector(77, 53), App.asset.next_icon, just_h='C', just_w='L')
        self.repeat_icon = Image(
            Vector(127, 55), App.asset.repeat_icon, just_w='R')
        self.playlist_position = Text(Vector(3, 59), justify='L')
        self.elements |= {self.progress_bar, self.timestamp_current, self.timestamp_total,
                          self.pause_icon, self.rewind_icon, self.next_icon, self.playlist_position}
        # Scheduling
        self._repeat_fut = core.Interface.loop.create_future()

    async def show(self):
        self.PLAYER.play()

    def refresh(self):
        super().refresh()
        self.c.execute("SELECT duration FROM tags WHERE id = ?",
                       [self.playlist[self.tracknumber][0]])
        _cur_duration = self.c.fetchone()[0]
        self.marquee.text = self.playlist[self.tracknumber][3]
        self.progress_bar.pos2 = Vector(App.constrain(
            self.playlist[self.tracknumber][-1].duration('s'), 0, _cur_duration, 3, 125), 40)
        self.timestamp_current.text = App.constrain_time(
            self.playlist[self.tracknumber][-1].duration('s'))
        self.timestamp_total.text = App.constrain_time(_cur_duration)
        self.playlist_position.text = f"{self.tracknumber+1}/{len(self.playlist)}"

    def render(self):
        if self._repeat_flag:
            core.interface.render(self.repeat_icon)
        super().render()

    def repeat(self, count: int):
        self._repeat_flag = True
        if count > 0:
            for i in range(count):
                self._copy()
        else:
            self._repeat_fut = core.Interface.schedule(
                self._repeat(self.PLAYER.active))

    async def _repeat(self, track):
        await track.wait(-10, "s")
        self._repeat_fut = core.Interface.schedule(self._repeat(self._copy))

    def _fill(self, playlist):
        for i, track in enumerate(playlist):
            track = list(track)
            track.append(player.Track(track[2]))
            core.Interface.schedule(self._next(track[-1]))
            playlist[i] = track
            self.PLAYER.append(track[7], False)
        return playlist

    def _copy(self):
        copy = self.playlist[self.tracknumber].copy()
        copy[-1] = player.Track(current[2])
        self.playlist.insert(self.tracknumber + 1, copy)
        return copy[-1]

    async def _next(self, track):
        await track
        if self.tracknumber - len(self.playlist) - 1:
            self.tracknumber += 1
        else:
            self.playerstate, self.pause_icon.image = False, App.asset.play_icon


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.powersaving()
            if window._repeat_flag:
                window._repeat_fut.cancel()
                window._repeat_fut = core.Interface.loop.create_future()
            if window.tracknumber != len(window.playlist) - 1:
                window.PLAYER.skip()

        async def left(null, window: Main):
            window._copy()
            await Handle.press.right(None, window)

        async def centre(null, window: Main):
            window.powersaving()
            window.pause_icon.image = App.asset.play_icon if window.playerstate else App.asset.pause_icon
            if window.playerstate:
                window.PLAYER.pause()
            else:
                window.PLAYER.play()
            window.playerstate = not window.playerstate

        async def up(null, window: Main):
            window.powersaving(cancel=True)
            await Options(window)
            window.powersaving()

        async def down(null, window: Main):
            window.PLAYER.clear()
            window.PLAYER.cancel(window.playlist[window.tracknumber][-1])
            window._finish()


class Options(menu.Menu):

    def __init__(self, player: Main):
        self.player = player
        _elements = [
            menu.MenuElement(Text(Vector(0, 0), "Set Sleep Timer", justify='L'),
                             func=self._sleeptimer),
            menu.MenuElement(Text(Vector(0, 0), "Enable Repeat", justify='L'),
                             data=("Enable Repeat?", "Repeat?", True),
                             func=self._repeat),
            menu.MenuElement(Text(Vector(0, 0), "Rescan Device", justify='L'),
                             func=self._rescan)]
        super().__init__(*_elements, title="Player Options")

    async def _sleeptimer(self, data):
        val = await numpad.Numpad(0, 180, 30, title="Sleep Timer") * 60
        if val != 0:
            self.player._sleeptimer = core.Interface.schedule(
                self.player.sleeptimer(val))

    async def _repeat(self, data):
        count = await numpad.Numpad(-1, 10, 1, title="Repeat: -1 for inf")
        if count != 0:
            self.player.repeat(count)

    async def _rescan(self, data):
        res = await query.Query("Re-scan Device?", "Rescan", cancel=True)
        if res:
            App.var.rescan = True
