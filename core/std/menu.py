from ..render.window import Window 
from ..interface import Interface 
from ..input.event import Handler
from ..render.element import Text
from ..vector import Vector

async def null(self, window):
    pass

class MenuElement:

    X_OFFSET = 3
    Y_OFFSET = 15

    def __init__(self, *elements, data=None, func=null):
        self.data = data
        self._index = -1
        self.elements = elements
        self._rel_pos = [element.anchor for element in self.elements]

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self, index, offset):
        if index != self._index:
            self._index = index
            for i, element in enumerate(self.elements):
                element.anchor = self._rel_pos[i] core.Vector(X_OFFSET, Y_OFFSET + offset * self._index)

class Menu(Window):

    CURSORS = {
        "none" : Text(Vector(0, 0), "", justify='R'),
        "default" : Text(Vector(0, 0), "<", justify='R'),
        "large" : Text(Vector(0, 0), "<-", justify='R')
    }

    def __init__(self, *items: MenuElement, visable=4, offset=11, title="Menu", end=True, cursor="default"):
        self._visible = visable
        self._elements = list(items)
        if end:
            self._elements.append(MenuElement(Text(Vector(0, 0), "Return", justify="L"), func=lambda self, window: window.finish()))
        for element in self._elements:
            element.offset = offset
        self._c_elements = []
    
        self._index = 0
        self._c_index = self._index

        self.title = Text(Vector(3, 5), title, justify='L')
        self.cursor = self.CURSORS[cursor].copy()



        
