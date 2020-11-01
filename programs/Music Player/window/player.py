import core
import time
import sqlite3
import player
import asyncio
import traceback #REEMMOMVE MEMEMEM
from app import App
from core import Vector
from core.std import menu, numpad, query
from core.render.element import Text, Line, Image, Marquee

class Main(core.render.Window):

    def __init__(self, db, playlist):
        self.db = db
        self.c = self.db.cursor()
        self.player = player.main
        self.playerstate = True
        self.tracknumber = 0
        for i, track in enumerate(playlist):
            track = list(track)
            track.append(player.Track(track[2]))
            core.Interface.schedule(self.next(track[-1]))
            playlist[i] = track
            self.player.append(track[7])
        self.playlist = playlist
        self.elements = [
            Text(Vector(64 ,5)), # Title 0 
            Text(Vector(127, 5), justify='R'), # Battery 1 
            Line(Vector(0, 9), Vector(128, 9)), # 2
            Text(Vector(3, 15), justify='L'), # Volume 3
            Marquee(Vector(64, 32), width=16), # Track Description 4
            Line(Vector(3, 40), Vector(3, 40), width=2), # Track Position Indicator 5
            Text(Vector(3, 45), justify='L'), # Current Track Position 6
            Text(Vector(127, 45), justify='R'), # Track Length 7
            Image(Vector(64, 55), App.asset.pause_icon), # Play / Pause Icon 8
            Image(Vector(40, 55), App.asset.rewind_icon), # Rewind Track Icon 9
            Image(Vector(80, 55), App.asset.next_icon),  # Next Track Icon 10
            Text(Vector(3, 55), justify='L'),  # Playlist Position Indicator 11
            Image(Vector(127, 15), App.asset.sleep_icon, just_w='R', just_h='C'), # Sleep Timer Icon 12
            Image(Vector(127, 60), App.asset.repeat_icon, just_w='R', just_h='C')] # Repeat Timer Icon 13
        App.interval(self.refresh)
        super().__init__()
    
    async def show(self):
        self.timeout = core.Interface.schedule(self.powersaving())
        self.refresh()
    
    def refresh(self):
        _e = self.elements
        _e[0].text = time.strftime("%I:%M%p")
        _e[1].text = f"{core.hw.Battery.percentage()}%"
        _e[3].text = f"{core.hw.Audio.current()}%"
        _e[4].text = self.playlist[self.tracknumber][3]
        self.c.execute("SELECT duration FROM tags WHERE id = ?", [self.playlist[self.tracknumber][0]])
        _e[5].pos2 = Vector(App.constrain(self.playlist[self.tracknumber][-1].duration('s'), 0, self.c.fetchone()[0], 3, 125), 40)
        _e[6].text = App.constrain_time(self.playlist[self.tracknumber][-1].duration('s'))
        self.c.execute("SELECT duration FROM tags WHERE id = ?", [self.playlist[self.tracknumber][0]])
        _e[7].text = App.constrain_time(self.c.fetchone()[0])
        _e[11].text = f"{self.tracknumber+1}/{len(self.playlist)}"
        self.elements = _e 
    
    def render(self):
        if True:
            core.interface.render(self.elements[12])
        if True:
            core.interface.render(self.elements[13])
        for element in self.elements[:11]: # Only Non Conditional Elements
            core.interface.render(element)

    async def powersaving(self):
        print("Function Called")
        if self.timeout.done():
            core.hw.Backlight.fill(core.sys.var.colour)
            core.Interface.application().render.enable()
        print("Waiting")
        print(f"For {App.const.screen_timeout}")
        await asyncio.sleep(App.const.screen_timeout)
        print("Executing")
        print([core.sys.var.colour, 0, 30])
        try:
            core.hw.Backlight.fill([core.sys.var.colour, 0, 30])
            print("Next") 
            core.hw.Backlight.fill([248, 36, 41])
            core.Interface.application().render.disable()
        except Exception as e:
            print(e)
            traceback.print_exception(e, e, e.__traceback__)
        print("Completed")
    
    async def sleeptimer(self, time: int):
        await asyncio.sleep(time)
        core.hw.Power.halt()

    async def next(self, track):
        await track
        self.tracknumber += 1
        self.elements[4].reset()

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.timeout = core.Interface.schedule(window.powersaving())
            window.player.skip()

        async def left(null, window: Main):
            window.timeout = core.Interface.schedule(window.powersaving())

        async def centre(null, window: Main):
            window.timeout = core.Interface.schedule(window.powersaving())
            window.elements[8].image = App.asset.play_icon if window.playerstate else App.asset.pause_icon
            if window.playerstate:
                window.player.pause()
            else:
                window.player.play()
            window.playerstate = not window.playerstate

        async def up(null, window: Main):
            window.timeout = core.Interface.schedule(window.powersaving())
        
        async def down(null, window: Main):
            window.timeout = core.Interface.schedule(window.powersaving())

'''class Settings(menu.Menu):

    def __init__(self):
        _elements = [
            menu.MenuElement(Text(Vector(0, 0), "Set Sleep Timer"),
            data=(numpad, ("Enable Repeat", "Repeat?")),
            func= self.select),
            menu.MenuElement(Text(Vector(0, 0), "Enable Repeat"),
            data= (query, (0, 90, 30, "Set Sleep Timer")),
            func= self.)]
        super().__init__(*_elements, title="Player Settings")
    
    async def select(self, data):
        await data[0](*data[1])'''
