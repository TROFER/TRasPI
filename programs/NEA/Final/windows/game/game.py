import core
from windows.game.stage import Room
from app import App


class Game(core.render.Window):

    def __init__(self):
        super().__init__()
        self.scoring = {
            "score" : 0,
            "depth_multiplier" : 1,
            "surface_exit" : True
        }
        self._flag = True
        App.interval(self.check_flag)

    def render(self):
        pass

    async def show(self):
        if self._flag:
            start = Room(self)
            start.generate()
            self._flag = False
            await start
        else:
            self.finish()
    
    def check_flag(self):
        if self._flag:
            self.finish()

    def print_debug(self):
        print(f"[G]: Score: {self.scoring['score']} Multiplier: {self.scoring['depth_multiplier']}")