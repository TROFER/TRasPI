import random
import threading

import core
from app import App
from server import server
from windows.game.results import Results
from windows.game.stage import Room

from game.library import lib


class Game(core.render.Window):

    def __init__(self):
        super().__init__()
        self.scoring = {
            "score": 0,
            "depth_multiplier": 1,
            "surface_exit": True,
            "golden_keys" : 0
        }
        self.active_window = None
        self._flag = 1

        # Start Telemetery Server
        self.start_server()

        # Load Sprites
        self.sprites = {}

        if App.var.playerskin is None or App.const.rebuild_library:
            type_id = lib.fetch_typeid("texture", "player-skin")
            lib.databases["textures"].c.execute(
                "SELECT image_id FROM texture WHERE type_id = ?", [type_id])
            image_id = random.choice(lib.databases["textures"].c.fetchall())[0]
            App.var.playerskin = image_id
        self.sprites["player"] = lib.fetch_image(App.var.playerskin)

        type_id = lib.fetch_typeid("texture", "goldenkey")
        self.sprites["goldenkey"] = lib.fetch_texture(type_id)

        type_id = lib.fetch_typeid("texture", "goldenkey-notify")
        self.sprites["goldenkey-notify"] = lib.fetch_texture(type_id)

        type_id = lib.fetch_typeid("texture", "newroom-notify")
        self.sprites["newroom-notify"] = lib.fetch_texture(type_id)

        # Flag Checking
        App.interval(self.check_flag)

    def render(self):
        pass

    async def show(self):
        # Set Backlight
        core.hw.Backlight.fill((57, 99, 100), force=True)
        core.hw.Key.all(False)

        # Window Logic
        if self._flag == 1:
            self._flag = 2
            start = Room(self)
            start.generate()
            await start
        elif self._flag == 2:
            self._flag = 3
            results = Results(self)
            await results
        else:
            self.server.stop()
            self.serverthread.join()
            self.finish()

    def check_flag(self):
        if self._flag:
            self.finish()

    def start_server(self):
        try:
            self.server = server.Server(self.generate_debug)
            self.serverthread = threading.Thread(
                target=self.server.await_requests, daemon=True)
            self.serverthread.start()
        except OSError:
            pass

    def generate_debug(self):
        stats = {"score": self.scoring['score'],
                 "multiplier": self.scoring['depth_multiplier'],
                 "golden_keys" : self.scoring['golden_keys']}
        try:
            stats.update(self.active_window.debug())
        except AttributeError:
            pass
        return stats
