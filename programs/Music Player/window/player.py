import core
import time
import player
import asyncio
from app import App
from core import Vector
from core.std import menu, numpad, query
from core.render.element import Text, Line, Image, Marquee

class Base(core.render.Window):

    PLAYER = player.main

    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()
        self._sleeptimer = None
        self.playerstate = True
        # Elements
        self.title = Text(Vector(64, 5))
        self.battery_icon = Image(Vector(1, 3), App.asset.battery_icon, just_w='L')
        self.battery_percentage = Text(Vector(13, 5), justify='L')
        self.title_line = Line(Vector(0, 9), Vector(128, 9))
        self.volume_percentage = Text(Vector(127, 14), justify='R')
        self.sleep_icon = Image(Vector(1, 11), App.asset.sleep_icon, just_w='L')
        self.marquee = Marquee(Vector(64, 32), width=20)
        self.elements = {self.title, self.battery_icon, self.battery_percentage, self.title_line, self.volume_percentage, self.marquee}
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
        await asyncio.sleep(App.const.screen_timeout)
        core.hw.Backlight.fill([core.sys.var.colour, 99, 25], force=True)

    def powersaving(self, cancel=False):
        self.timeout.cancel()
        if not cancel:
            self.timeout = core.Interface.schedule(self._powersaving(self.timeout))
    
    async def sleeptimer(self, time: int):
        await asyncio.sleep(time)
        core.hw.Power.halt()

class Main(Base):

    def __init__(self, db, playlist):
        super().__init__(db)
        self.repeat = 0
        self.tracknumber = 0
        self.playlist = self.fill(playlist)
        self.progress_bar = Line(Vector(3, 40), Vector(3, 40), width=2)
        self.timestamp_current = Text(Vector(3, 46), justify='L')
        self.timestamp_total = Text(Vector(127, 46), justify='R')
        self.pause_icon = Image(Vector(64, 53), App.asset.pause_icon, just_h='C')
        self.rewind_icon = Image(Vector(52, 53), App.asset.rewind_icon, just_h='C', just_w='R')
        self.next_icon = Image(Vector(77, 53), App.asset.next_icon, just_h='C', just_w='L')
        self.repeat_icon = Image(Vector(127, 55), App.asset.repeat_icon, just_w='R')
        self.playlist_position = Text(Vector(3, 59), justify='L')
        self.elements |= {self.progress_bar, self.timestamp_current, self.timestamp_total, self.pause_icon, self.rewind_icon, self.next_icon, self.playlist_position}
        self._fill(playlist)
    
    def refresh(self):
        super().refresh()
        self.c.execute("SELECT duration FROM tags WHERE id = ?", [self.playlist[self.tracknumber][0]])
        _cur_duration = self.c.fetchone()[0]
        self.marquee.text = self.playlist[self.tracknumber][3]
        self.progress_bar.pos2 = Vector(App.constrain(self.playlist[self.tracknumber][-1].duration('s'), 0, _cur_duration, 3, 125), 40)
        self.timestamp_current.text = App.constrain_time(self.playlist[self.tracknumber][-1].duration('s'))
        self.timestamp_total.text = App.constrain_time(_cur_duration)
        self.playlist_position.text = f"{self.tracknumber+1}/{len(self.playlist)}"
    
    def render(self):
        if self.repeat > 0:
            core.interface.render(self.repeat_icon)
        super().render()
    
    def _fill(self, playlist):
        for i, track in enumerate(playlist):
            track = list(track)
            track.append(player.Track(track[2]))
            core.Interface.schedule(self._next(track[-1]))
            playlist[i] = track
            self.PLAYER.append(track[7])
        return playlist

    async def _next(self, track):
        if self.repeat != 0:
            self.repeat -= 1
            self.PLAYER.next(player.Track(self.playlist[self.tracknumer][-1]))
        else:
            await track
            self.tracknumber += 1
    
class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.powersaving()
            window.PLAYER.skip()

        async def left(null, window: Main):
            window.PLAYER.next(player.Track(window.playlist[window.tracknumber][2]))
            window.PLAYER.skip()
            window.powersaving()

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
        
        async def down(null, window: Main): # Discuss with T
            window.powersaving(cancel=True)
            window.PLAYER.clear()
            window.PLAYER.cancel(window.playlist[window.tracknumber][-1])
            if window._sleeptimer is not None:
                window._sleeptimer.cancel()
            window.finish()

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
            self.player._sleeptimer = core.Interface.schedule(self.player.sleeptimer(val))

    async def _repeat(self, data):
        res = await query.Query("Enable Repeat?", "Repeat", cancel=True)
        if res:
            count = await numpad.Numpad(-1, 10, 1, title="Repeat: -1 for inf")
            self.player.repeat = count

    async def _rescan(self, data):
        res = await query.Query("Re-scan Device?", "Rescan", cancel=True)
        if res:
            App.var.rescan = True
