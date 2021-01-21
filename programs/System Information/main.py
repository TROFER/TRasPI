import core
from app import App
from windows import cpu, memory, network, storage, battery
from remote import main as remote

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.map = [cpu.Main(), memory.Main(), network.Main(), storage.Main(), battery.Main(), remote.Main()]

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