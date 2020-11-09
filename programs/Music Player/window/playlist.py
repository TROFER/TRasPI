import core
from core import Vector
from core.render.element import Marquee
from core.std import menu

from window import player


class Main(menu.Menu):

    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()
        _elements = []
        self.c.execute("SELECT * FROM playlist")
        for _playlist in self.c.fetchall():
            self.c.execute(
                f"SELECT count(*) FROM playlist_items WHERE playlist_id = ?", [_playlist[0]])
            _items = self.c.fetchone()[0]
            if _items != 0:
                _elements.append(self.elm(
                    mq := Marquee(Vector(0, 0), f"{_playlist[1]} ({_items}) {' '*18}", width=18, justify='L', flag=False, speed=0.5),
                    data=(self.db, _playlist),
                    func=self.__select,
                    on_hover=mq.play,
                    on_dehover=lambda mq: (mq[3].pause(), mq[3].reset())))
        super().__init__(*_elements, title="PLaylists - Music Pl...")

    async def __select(self, data):
        self.c.execute(
            "SELECT track_id FROM playlist_items WHERE playlist_id = ?", [data[1][0]])
        _tracks = []
        for _track_id in self.c.fetchall():
            self.c.execute("SELECT * FROM track WHERE id = ?", [_track_id[0]])
            _tracks.append(self.c.fetchone())
        await player.Main(self.db, _tracks)


class Handle(core.input.Handler, menu.Menu):

    window = Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
