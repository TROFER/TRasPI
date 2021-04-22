import core
from windows.game.stage import Room
from windows.game.results import Results
from app import App



class Game(core.render.Window):

    def __init__(self):
        super().__init__()
        self.scoring = {
            "score" : 0,
            "depth_multiplier" : 1,
            "surface_exit" : True
        }
        self._flag = 1
        App.interval(self.check_flag)

    def render(self):
        pass

    async def show(self):
        # Set Backlight
        core.hw.Backlight.fill((33, 94, 100), force=True)
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
            self.finish()
    
    def check_flag(self):
        if self._flag:
            self.finish()

    def print_debug(self):
        print(f"[G]: Score: {self.scoring['score']} Multiplier: {self.scoring['depth_multiplier']}")