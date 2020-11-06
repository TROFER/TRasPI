import core
from core.std import menu
from core.render.element import Marquee, Image, Text
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

class Player(player.Base):

    def __init__(self, db, station):
        super().__init__(db)
        self.station = station
        self.stop_icon = Image(Vector(64, 53), App.asset.stop_icon, just_h='C')
        self.elements |= {self.stop_icon}
    
    def render(self):
        for element in self.elements:
            core.Interface.render(element)
    
    def refresh(self):
        super().refresh()
        self.marquee.text = "TEST TEST TEST TEST" # NEED COMMAND

class Handle(core.input.Handler):

    window = Player

    class press:
        async def right(null, window: Player):
            window.powersaving()

        async def left(null, window: Player):
            window.powersaving()

        async def centre(null, window: Player):
            window.powersaving()
            window.pause_icon.image = App.asset.play_icon if window.playerstate else App.asset.stop_icon
            if window.playerstate:
                pass # Pause
            else:
                pass # Play
            window.playerstate = not window.playerstate

        async def up(null, window: Player):
            await Options(window)
            window.powersaving()

        async def down(null, window: Player):  # Discuss with T
            window.powersaving(cancel=True)
            # Stop & Clear
            if window._sleeptimer is not None:
                window._sleeptimer.cancel()
            window.finish()

class Options(menu.Menu):

    def __init__(self, player: Player):
        self.player = player
        _elements = [
            menu.MenuElement(Text(Vector(0, 0), "Set Sleep Timer", justify='L'),
            func=self._sleeptimer),
            menu.MenuElement(Text(Vector(0, 0), "Rescan Device", justify='L'),
            func=self._rescan)]
        super().__init__(*_elements, title="Player Options")
    
    async def _sleeptimer(self, data):
        val = await numpad.Numpad(0, 180, 30, title="Sleep Timer") * 60
        if val != 0:
            self.player._sleeptimer = core.Interface.schedule(self.player.sleeptimer(val))

    async def _rescan(self, data):
        res = await query.Query("Re-scan Device?", "Rescan", cancel=True)
        if res:
            App.var.rescan = True
