import core
from library import Library
from app import App
from window import browser

############## TRASPI MUSIC PLAYER ###############
## Version: 1.1                                 ##
## Created By: Tristan Day                      ##
## Date: 2020                                   ##
##################################################

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.library = Library()
        self._flag = True
        self.index = 0
        self.map = [browser.Top(self.library.db, "genre", title="Genres - Music Pl...")]
    
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
