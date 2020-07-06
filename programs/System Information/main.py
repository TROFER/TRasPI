from app import App
import core
import cpu
#import memory
#import network
#import storage
#import hardware

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.map = [cpu.Main()]
        ''' , memory.Main,
                     network.Main, storage.Main, hardware.Main '''

    async def show(self):
        if self._flag:
            self._flag = False
            res = await self.map[self.index]
            if res is None:
                self.finish()
            else:
                self.index = (self.index + res) % len(self.map)

App.window = Main
main = App