import core
import time
import datetime
import sqlite3
from player import player
from app import App
from core import Vector
from core.std import menu, numpad, query
from core.render.element import Text, Line, Image, Marquee

class Main(core.render.Window):

    def __init__(self, db, playlist): # Playlist = List of track id's
        self.db = db
        self.c = self.db.cursor()
        self.playerstate = 0
        self.tracknumber = 0
        self.playlist = playlist 
        self.tracks = []
        for path in self.playlist[self.tracknumber][2]:
            track = player.track(path)
            core.Interface.schedule(self.increment(track))
            player.append(track), self.tracks.append(track)
        
        self.c_elements = [
            Image(Vector(127, 15), App.asset.sleep_icon, just_w='R', just_h='C'), # Sleep Timer Indicator
            Image(Vector(127, 60), App.asset.repeat_icon, just_w='R', just_h='C')] # Repeat Icon
        self.elements = [
            Text(Vector(64 ,5)), # Title 0 
            Text(Vector(127, 5), justify='R'), # Battery 1 
            Line(Vector(0, 9), Vector(128, 9)),
            Text(Vector(3, 15), justify='L'), # Volume 4
            Marquee(Vector(64, 32), width=16), # Track Description 5
            Line(Vector(3, 40), Vector(3, 40), width=2), # Track Position Indicator 6
            Text(Vector(3, 45), justify='L'), # Current Track Position 7
            Text(Vector(127, 45), justify='L'), # Track Length 8
            Image(Vector(64, 55), App.asset.pause_icon, just_h='C'), # Play / Pause Icon 9
            Image(Vector(40, 55), App.asset.rewind_icon, just_h='C'), # Rewind Track Icon 10
            Image(Vector(80, 55), App.asset.next_icon, just_h='C'),  # Next Track Icon 11
            Text(Vector(3, 60), justify='L')] # Playlist Position Indicator 12
        App.interval(self.refresh())
    
    async def show(self):
        self.refresh()
    
    def refresh(self):
        _e = self.elements
        _e[0].text = time.strftime("%I:%M%p")
        _e[1].text = core.hw.Battery.percentage + " %"
        _e[4].text = core.hw.Audio.current + " %"
        _e[5].text = self.playlist[self.tracknumber][3]
        _e[6].pos2 = 0 # <----------- INSERT FUNCTION HERE
        _e[7].text = str(datetime.timedelta(seconds=0)) # <----------- INSERT FUNCTION HERE
        self.c.execute("SELECT duration FROM tags WHERE id = ?", self.playlist[self.tracknumber][0])
        _e[8].text = str(datetime.timedelta(seconds=self.c.fetchone()[0]))
        _e[9].image = App.asset.pause_icon if self.playerstate == 2 else App.asset.play_icon
        _e[12].text = f"{self.tracknumber+1}/{len(self.playlist)}"
        self.elements = _e 
    
    def render(self):
        if True:
            core.interface.render(self.c_elements[0])
        if True:
            core.interface.render(self.c_elements[1])
        for element in self.elements:
            core.interface.render(element)
    
    async def increment(self, track):
        await track
        self.tracknumber += 1


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            player.skip()

        async def left(null, window: Main):
            pass # 

        async def centre(null, window: Main):
            pass # Play / Pause

        async def up(null, window: Main):
            pass # Player Menu

class Menu(menu.Menu):

    def __init__(self):
        _elements = [
            menu.MenuElement(Text(Vector(0, 0), "Set Sleep Timer"),
            data=(numpad, ("Enable Repeat", "Repeat?")),
            func= self.select),
            menu.MenuElement(Text(Vector(0, 0), "Enable Repeat")
            data= (query, (0, 90, 30, "Set Sleep Timer")),
            func= self.select)]
        super().__init__(*_elements, title="Player Settings")
    
    async def select(self, data):
        await data[0](*data[1])