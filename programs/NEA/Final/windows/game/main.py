import core
from windows.game.room import Room


class Game(core.render.Window):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.debug_cache = ""

    def render(self):
        pass

    async def show(self):
        start = Room(self)
        start.generate()
        await start
        self.finish()
        # Results screen?
    
    def print_debug(self):
        print(f"[G]: Score: {self.score}")