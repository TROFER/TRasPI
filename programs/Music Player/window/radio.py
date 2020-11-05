import core
from core.std import menu
from core.render.element import Marquee
from core import Vector
from window import player

class Top(menu.Menu):

    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()
        _elements = []
        self.c.execute("SELECT * FROM genre")
        for _genre in self.c.fetchall():
            self.c.execute(f"SELECT count(*) FROM radio WHERE genre_id = ?", [_genre[0]])
            _items = self.c.fetchone()[0]
            if _items != 0:
                    _elements.append(self.elm(
                        mq:= Marquee(Vector(0, 0), f"{_genre[1]} ({_items}) {' '*18}", width=18, justify='L', flag=False, speed=0.5),
                        data= (self.db, _genre),
                        func= Bottom,
                        on_hover= mq.play,
                        on_dehover= lambda  mq: (mq[3].pause(), mq[3].reset())))
        super().__init__(*_elements, title="Radio - Music Pl...")

class Bottom(menu.Menu):

    def __init__(self, db, genre):
        self.db = db
        self.c = self.db.cursor()
        _elements = []
        self.c.execute("SELECT * FROM radio WHERE genre_id = ?", [genre[0]])
        stations = self.c.fetchall()
        for _station in stations:
            _elements.append(self.elm(
                mq:= Marquee(Vector(0, 0), f"{_station[2]} {' '*18}", width=18, justify='L', flag=False, speed=0.5),
                data= (self.db, _station),
                on_hover= mq.play,
                on_dehover= lambda mq: (mq[3].pause(), mq[3].reset())))
        super().__init__(*_elements, title=f"Radio - {genre[0]} - Mu...")

class Player(core.render.Window, player.Base):

    def __init__(self, db, station):
        super().__init__()
        super(player.Base, self).__init__(db)
        self.station = station
    
    def render(self):
        for element in self.elem
    
    def refresh(self):
        pass

