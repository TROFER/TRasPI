import core
import time
import datetime
import sqlite3
from app import App
from core import Vector
from core.render.element import Text, Line, Image, Marquee

class Main(core.render.Window):

    def __init__(self, db, playlist): # Playlist = List of track id's
        self.db = db
        self.c = self.db.cursor()
        self.c_elements = [
            Image(Vector(127, 15), App.asset.sleep_icon, just_w='R', just_h='C'), # Sleep Timer Indicator
            Image(Vector(127, 60), App.asset.repeat_icon, just_w='R', just_h='C')] # Repeat Icon
        self.elements = [
            Text(Vector(64 ,5)), # Title 0 
            Text(Vector(127, 5), justify='R'), # Battery 1 
            Line(Vector(0, 9), Vector(128, 9)),
            Text(Vector(3, 15), justify='L') # Volume 4
            Marquee(Vector(64, 32), width=16), # Track Description 5
            Line(Vector(3, 40), Vector(3, 40), width=2), # Track Position Indicator 6
            Text(Vector(3, 45), justify='L'), # Current Track Position 7
            Text(Vector(127, 45), justify='L'), # Track Length 8
            Image(Vector(64, 55), App.asset.pause_icon, just_h='C'), # Play / Pause Icon 9
            Image(Vector(40, 55), App.asset.rewind_icon, just_h='C'), # Rewind Track Icon 10
            Image(Vector(80, 55), App.asset.next_icon, just_h='C'),  # Next Track Icon 11
            Text(Vector(3, 60), justify='L')] # Playlist Position Indicator 12
        App.interval(self.refresh(), 1)
    
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

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            pass # NEXT

        async def left(null, window: Main):
            pass # SKIP

        async def centre(null, window: Main):
            pass # Play / Pause

        async def up(null, window: Main):
            pass # Player Menu
