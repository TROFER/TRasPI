import core
import time
import sqlite3
import player
import asyncio
from app import App
from core import Vector
from core.std import menu, numpad, query
from core.render.element import Text, Line, Image, Marquee, Rectangle

class Main(core.render.Window):

    def __init__(self, db, playlist):
        self.timeout = core.Interface.loop.create_future()
        self._sleeptimer = None
        self.db = db
        self.c = self.db.cursor()
        self.player = player.main
        self.repeat = 0
        self.playerstate = True
        self.tracknumber = 0
        for i, track in enumerate(playlist):
            track = list(track)
            track.append(player.Track(track[2]))
            core.Interface.schedule(self._next(track[-1]))
            playlist[i] = track
            self.player.append(track[7])
        self.playlist = playlist
        self.elements = [
            Text(Vector(64 ,5)), # Title 0 
            Image(Vector(1, 3), App.asset.battery_icon, just_w='L'),
            Text(Vector(13, 5), justify='L'), # Battery 1 
            Line(Vector(0, 9), Vector(128, 9)), # 2
            Text(Vector(127, 14), justify='R'), # Volume 3
            Marquee(Vector(64, 32), width=20), # Track Description 4
            Line(Vector(3, 40), Vector(3, 40), width=2), # Track Position Indicator 5
            Text(Vector(3, 46), justify='L'), # Current Track Position 6
            Text(Vector(127, 46), justify='R'), # Track Length 7
            Image(Vector(64, 53), App.asset.pause_icon, just_h='C'), # Play / Pause Icon 8
            Image(Vector(52, 53), App.asset.rewind_icon, just_h='C', just_w='R'), # Rewind Track Icon 9
            Image(Vector(77, 53), App.asset.next_icon, just_h='C', just_w='L'),  # Next Track Icon 10
            Text(Vector(3, 55), justify='L'),  # Playlist Position Indicator 11
            Image(Vector(1, 11), App.asset.sleep_icon, just_w='L'), # Sleep Timer Icon 12
            Image(Vector(127, 55), App.asset.repeat_icon, just_w='R')] # Repeat Timer Icon 13
        App.interval(self.refresh)
        super().__init__()
    
    async def show(self): 
        self.powersaving()
        self.refresh()
    
    def refresh(self):
        _e = self.elements
        _e[0].text = time.strftime("%I:%M%p")
        _e[2].text = f"{core.hw.Battery.percentage()}%"
        _e[4].text = f"{core.hw.Audio.current()}%"
        _e[5].text = self.playlist[self.tracknumber][3]
        self.c.execute("SELECT duration FROM tags WHERE id = ?", [self.playlist[self.tracknumber][0]])
        _e[6].pos2 = Vector(App.constrain(self.playlist[self.tracknumber][-1].duration('s'), 0, self.c.fetchone()[0], 3, 125), 40)
        _e[7].text = App.constrain_time(self.playlist[self.tracknumber][-1].duration('s'))
        self.c.execute("SELECT duration FROM tags WHERE id = ?", [self.playlist[self.tracknumber][0]])
        _e[8].text = App.constrain_time(self.c.fetchone()[0])
        _e[12].text = f"{self.tracknumber+1}/{len(self.playlist)}"
        self.elements = _e 
    
    def render(self):
        if self._sleeptimer is not None:
            core.interface.render(self.elements[13])
        if self.repeat > 0:
            core.interface.render(self.elements[14])
        for element in self.elements[:12]: # Only Non Conditional Elements
            core.interface.render(element)

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

    async def _next(self, track):
        if self.repeat != 0:
            self.repeat -= 1
            self.player.next(player.Track(self.playlist[self.tracknumer][-1]))
        else:
            await track
            self.tracknumber += 1
    
class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.powersaving()
            window.player.skip()

        async def left(null, window: Main):
            window.player.next(player.Track(window.playlist[window.tracknumber][2]))
            window.player.skip()
            window.powersaving()

        async def centre(null, window: Main):
            window.powersaving()
            window.elements[9].image = App.asset.play_icon if window.playerstate else App.asset.pause_icon
            if window.playerstate:
                window.player.pause()
            else:
                window.player.play()
            window.playerstate = not window.playerstate

        async def up(null, window: Main):
            window.powersaving(cancel=True)
            await Options(window)
            window.powersaving()
        
        async def down(null, window: Main): # Discuss with T
            window.powersaving(cancel=True)
            window.player.clear()
            window.player.cancel(window.playlist[window.tracknumber][-1])
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
        self.finish()

    async def _repeat(self, data):
        res = await query.Query("Enable Repeat?", "Repeat", cancel=True)
        if res:
            count = await numpad.Numpad(-1, 10, 1, title="Repeat: -1 for inf")
            self.player.repeat = count
        self.finish()

    async def _rescan(self, data):
        res = await query.Query("Re-scan Device?", "Rescan", cancel=True)
        if res:
            App.var.rescan = True
        self.finish()