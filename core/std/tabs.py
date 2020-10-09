from ..render.window import Window

class TabManager(Window):

    tabs = []

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.tabs = self.__class__.tabs.copy()

    async def show(self):
        if self._flag:
            self._flag = False
            while True:
                res = await self.tabs[self.index]
                if isinstance(res, int):
                    self.index = (self.index + res) % len(self.tabs)
                else:
                    self.finish()
                    break
            self._flag = True

