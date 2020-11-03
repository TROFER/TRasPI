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
                func=self.playall),
            menu.MenuElement(
                Text(Vector(0, 0), "Shuffle All", justify='L'),
                func=self.shuffle)]
        self.c.execute(f"SELECT * FROM {filter}")
        for group in self.c.fetchall():
            self.c.execute(f"SELECT count(*) FROM track WHERE {_fieldname} = ?", [group[0]])
            _elements.append(self.elm(
                mq:= Marquee(Vector(0, 0), f"{group[1]} ({self.c.fetchone()[0]}) {' '*18}", width=18, justify='L', flag=False, speed=0.5),
                data= (_fieldname, group[0], group[1], mq),
                func= self.select,
                on_hover=mq.play,
                on_dehover=lambda mq: (mq[3].pause(), mq[3].reset())))
        super().__init__(*_elements, title=title)
    
    async def playall(self, data):
        self.c.execute("SELECT * FROM track")
        tracks = self.c.fetchall()
        await player.Main(self.db, tracks)
        
    async def shuffle(self, data):
        self.c.execute("SELECT * FROM track")
        _tracks = self.c.fetchall()
        random.shuffle(_tracks)
        await player.Main(self.db, _tracks)
    
    async def select(self, filter):
        await Bottom(self.db, filter, filter[2])


class Handle(core.input.Handler, menu.Menu):

    window = Top

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)

class Bottom(menu.Menu):

    def __init__(self, db, filter: str, title):
        self.db = db
        self.c = db.cursor()
        self.filter = filter
        _elements = [
            menu.MenuElement(
                Text(Vector(0, 0), "Play All", justify='L'),
                func=self.playall),
            menu.MenuElement(
                Text(Vector(0, 0), "Shuffle All", justify='L'),
                func=self.shuffle)]
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        for track in self.c.fetchall():
            _elements.append(self.elm(
                mq := Marquee(Vector(0, 0), f"{track[1]}{' '*18}", width=18, justify='L', flag=False, speed=0.5),
                data= (track, mq),
                func= self.select,
                on_hover=mq.play,
                on_dehover=lambda mq: (mq[1].pause(), mq[1].reset())))
        super().__init__(*_elements, title=f"{self.filter[0][:-3].capitalize()} - {title}")

    async def playall(self, data):
        self.c.execute(
            f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        await player.Main(self.db, self.c.fetchall())

    async def shuffle(self, data):
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        _tracks = self.c.fetchall()
        random.shuffle(_tracks)
        await player.Main(self.db, _tracks)
    
    async def select(self, data):
        await player.Main(self.db, [data[0]])


class Handle(core.input.Handler, menu.Menu):

    window = Bottom

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
