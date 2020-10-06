from app import App
from window import single, playlist, radio
from index import Index
import core 

###############TRASPI MUSIC PLAYER################
## Created By: Tristan Day                      ##
## Date: 2020                                   ##
################################################## 

rescan = True


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.check_rescan()
        self._flag = True
        self.index = 0
        self.map = [single.main()]

    def rescan(self, force=False):
        if App.var.rescan or force:
            App.var.library = Index.scan()
            if App.var.directories:
                for directory in App.const.directories:
                    App.var.library = App.var.library + Index.scan(path=directory)
            App.var.rescan = False

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
