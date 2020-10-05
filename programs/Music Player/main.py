from app import App
from tabs import single, playlist, radio
import core 

###############TRASPI MUSIC PLAYER################
## Created By: Tristan Day                      ##
## Date: 2020                                   ##
################################################## 


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.map = []

    async def show(self):
        if self._flag:
            self._flag = False
            while True:
                res = await self.map[self.index]
                if res is None:
                    self.finish()
                    break
                else:
                    self.index = (self.index + res) % len(self.map)
            self._flag = True


App.window = Main
main = App
