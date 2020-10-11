from core.std import menu
from core.render.element import Text
from core import Vector
#from player import Player
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
                Text(Vector(0, 0), f"{group[1][:16]} ({self.c.fetchone()[0]+1})", justify='L'),
                data= (_fieldname, group[0]),
                func= self.select))
        super().__init__(*_elements, title=title)
    
    def playall(self):
        self.c.execute("SELECT * FROM track") 
        Player(self.fetchall())
    
    def shuffle(self):
        self.c.execute("SELECT * FROM track")
        Player(random.shuffle(self.fetchall()))
    
    def select(self, filter):
        Bottom(self.db, filter)

class Bottom(menu.Menu):

    def __init__(db, filter: str):
        self.db = db
        self.c = sb.cursor()
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
                Text(Vector(0, 0), track[1][:19], justify='L'),
                data= track,
                func= self.select))
        super().__init__(*elements, title=self.filter[0][:-3].capitalise())

    def playall(self):
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        Player(self.c.fetchall())
    
    def shuffle(self):
        self.c.execute(f"SELECT * FROM track WHERE {self.filter[0]} = ?", [self.filter[1]])
        Player(random.shuffle(self.c.fetchall()))

def Player(*args):
    pass