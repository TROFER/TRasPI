import core
from windows.game.stage import Room
from app import App


class Game(core.render.Window):

    def __init__(self):
        super().__init__()
        self.score = 0
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
        print(f"[G]: Score: {self.score}")