import core
import cpu, memory, network, storage, hardware

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.map = [cpu.main, memory.main, network.main, storage.main, hardware.main]
    
    async def show(self):
        if self._flag:
            self._flag = False
            res = await self.map[self.index]
            if res is None:
                self.finish()
            else:
                self.index = (self.index + res) % len(self.map) 
