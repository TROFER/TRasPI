from ..render.window import Window 
from ..interface import Interface 
from ..input.event import Handler
from ..render.element import Text, Line
from ..vector import Vector
from ..error.attributes import SysConstant
from typing import Callable

async def null(window):
    pass

class MenuElement:

    X_OFFSET = 3
    Y_OFFSET = 15

    def __init__(self, *elements, data=None, func: Callable=null, **on_calls: Callable):
        self.data = data
        self._index = -1
        self.elements = elements
        self._rel_pos = [element.anchor for element in self.elements]
        self.__calls = {"enter": func, **{k[3:]:v for k,v in on_calls.items() if k.startswith("on_")}}

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self, index, offset):
        if index != self._index:
            self._index = index
            for i, element in enumerate(self.elements):
                element.anchor = self._rel_pos[i] + Vector(self.X_OFFSET, self.Y_OFFSET + offset * self._index)

    async def _call(self, name: str="enter", halt=True):
        if (func := self.__calls.get(name, null)) is null:
            return
        if isinstance(func, Window):
            return await func
        fut = Interface.schedule(func, self.data)
        if halt:
            return await fut
        return fut

class Menu(Window):

    CURSORS = {
        "none" : Text(Vector(0, 0), "", justify='R'),
        "default" : Text(Vector(0, 0), "<", justify='R'),
        "large" : Text(Vector(0, 0), "<-", justify='R')
    }

    elm = MenuElement

    def __init__(self, *items: MenuElement, visable=5, offset=11, title="Menu", end=True, cursor="default"):
        self._visible = visable
        self._elements = list(items)
        if end:
            self._elements.append(self.elm(Text(Vector(0, 0), "Return", justify="L"), func=lambda data: self.finish()))
        # for element in self._elements:
        self._offset = offset
        self.__c_elements = []
    
        self.__index = 0
        self.__c_index = self.__index

        self.title = Text(Vector(3, 5), title, justify='L')
        self.title_line = Line(Vector(0, 9), Vector(128, 9))
        self.__cursor = self.CURSORS[cursor]

        super().__init__()

    async def show(self):
        self.regenerate()

    def regenerate(self):
        self.__c_elements = self._elements[self.__index:self.__index+self._visible]
        for index, elm in enumerate(self.__c_elements):
            elm.refresh(index, self._offset)
        self.__cursor.anchor = Vector(SysConstant.width - self.elm.X_OFFSET, (self._elements[self.__c_index]._index if self._elements else 0) * self._offset + self.elm.Y_OFFSET)

    def render(self):
        Interface.render(self.title), Interface.render(self.title_line)
        Interface.render(self.__cursor)
        for elm in self.__c_elements:
            for e in elm.elements:
                Interface.render(e)

    async def call(self):
        await self._elements[self.__c_index]._call()
        # await self._elements[self.__c_index]._call("return", False)

    async def hook(self, name: str, halt=False):
        return await self._elements[self.__c_index]._call(name, halt)

    async def move(self, direction: int):
        x = self._elements[self.__c_index]._call("dehover", False)
        y = await x
        self.__c_index = (self.__c_index + direction) % len(self._elements)
        if self.__c_index < self.__index:
            self.__index = self.__c_index
        elif self.__c_index >= self.__index + self._visible:
            self.__index = max(0, self.__c_index - (self._visible - 1))
        await self._elements[self.__c_index]._call("hover", False)
        self.regenerate()

class Handle(Handler):

    window = Menu

    class press:
        async def centre(null, window: Menu):
            await window.call()
        async def up(null, window: Menu):
            await window.move(-1)
        async def down(null, window: Menu):
            await window.move(1)
        async def left(null, window: Menu):
            await window.hook("left")
        async def right(null, window: Menu):
            await window.hook("right")