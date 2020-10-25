from core.std import menu
from core.render.element import Text, Marquee
from core import Vector
from window import player
import core
import random
import sqlite3

class Top(menu.Menu):

    def __init__(self, db, filter: str, title: str):
        self.db = db
        self.c = db.cursor()
        _fieldname = filter + "_id"
        _elements = [
            menu.MenuElement(
                Text(Vector(0, 0), "Play All", justify='L'),
                func= self.playall),
            menu.MenuElement(
                Text(Vector(0, 0), "Shuffle All", justify='L'),
                func= self.shuffle)]
        self.c.execute(f"SELECT * FROM {filter}")
        for group in self.c.fetchall():
            self.c.execute(f"SELECT count(*) FROM track WHERE {_fieldname} = ?", [group[0]])
            _elements.append(menu.MenuElement(
                Marquee(Vector(0, 0), f"{group[1][:16]} ({self.c.fetchone()[0]})", width=17, justify='L'),
                data= (_fieldname, group[0], group[1]),
                func= self.select))
        super().__init__(*_elements, title=title)
    
    async def playall(self):
        self.c.execute("SELECT * FROM track") 
        await player.Main(self.fetchall())
    
    async def shuffle(self):
        self.c.execute("SELECT * FROM track")
        await player.Main(random.shuffle(self.fetchall()))
    
    async def select(self, filter):
        await Bottom(self.db, filter, filter[2])


class Handle(core.input.Handler):

    window = Top

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
        
        async def centre(null, window):
            await window.call()
        
        async def up(null, window):
            await window.move(-1)
        
        async def down(null, window):
            await window.move(1)

class Bottom(menu.Menu):

    def __init__(self, db, filter: str, title):
        self.db = db
        self.c = db.cursor()
        self.filter = filter
        _elements = [
            menu.MenuElement(
                Text(Vector(0, 0), "Play All", justify='L'),
                func= self.playall),
            menu.MenuElement(
                Text(Vector(0, 0), "Shuffle All", justify='L'),
                func= self.shuffle)]
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        for track in self.c.fetchall():
            _elements.append(menu.MenuElement(
                Marquee(Vector(0, 0), track[1], width=18, justify='L'),
                data= track,
                func= self.select))
        super().__init__(*_elements, title=f"{self.filter[0][:-3].capitalize()} - {title}")

    async def playall(self):
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        await player.Main(self.c.fetchall())
    
    async def shuffle(self):
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        await player.Main(random.shuffle(self.c.fetchall()))
    
    async def select(self, data):
        await player.Main(self.db, [data])


class Handle(core.input.Handler):

    window = Bottom

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
        
        async def centre(null, window):
            await window.call()
        
        async def up(null, window):
            await window.move(-1)
        
        async def down(null, window):
            await window.move(1)

     
