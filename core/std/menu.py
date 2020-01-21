import core

__all__ = ["Menu", "MenuSingle"]

_ME_OFF_X = 3
_ME_OFF_Y = 15

class MenuElement:

    def __init__(self, *element: core.element, data={}, select=lambda self, window: None, hover=None, dehover=None):
        self.data = data
        self._elements = element
        self._rel_pos = [elm.pos for elm in self._elements]
        self._offset = 1
        self._index = -1
        self._select_func = select
        self._hover_func = lambda s, w: (hover) if hover is None else hover
        self._dehover_func = lambda s, w: (dehover) if dehover is None else dehover

    def _update(self, index):
        if index != self._index:
            self._index = index
            for i, elm in enumerate(self._elements):
                elm.pos = self._rel_pos[i] + core.Vector(_ME_OFF_X, _ME_OFF_Y + self._offset * self._index)

    def render(self):
        print("Render")
        for elm in self._elements:
            elm.render()

    def _select(self, window):
        return self._select_func(self, window)

    def _hover(self, window):
        return self._hover_func(self, window)

    def _dehover(self, window):
        return self._dehover_func(self, window)

class Menu(core.render.Window):

    Element = MenuElement
    template = core.asset.Template("std::window", path="window.template")

    def __init__(self, *items: MenuElement, visable=4, offset=core.asset.Font("std").size, title="Menu", end=True):
        self._visable = visable
        self._elements = list(items)
        if end:
            self._elements.append(MenuElement(core.element.Text(core.Vector(0, 0), "Return", justify="L"), select=lambda s, w: w.finish()))
        for elm in self._elements:
            elm._offset = offset
        self._c_elements = []

        self._index = 0
        self._c_index = self._index

        self._title = core.element.Text(core.Vector(3, 5), title, justify="L")
        self._cursor = core.element.Text(core.Vector(0, 0), "<", justify="R")

        self._update()

    def render(self):
        self._title.render()
        for elm in self._c_elements:
            elm.render()
        self._cursor.render()

    def _update(self):
        self._c_elements.clear()
        for index, elm in enumerate(self._elements[self._index:self._index + self._visable]):
            self._c_elements.append(elm)
            elm._update(index)
        self._cursor.pos = core.Vector(core.sys.WIDTH - _ME_OFF_X, _ME_OFF_Y + self._elements[self._c_index]._offset * self._elements[self._c_index]._index)

    def _down(self):
        if self._c_index < len(self._elements) - 1:
            self._elements[self._c_index]._dehover(self)
            self._c_index += 1
            if self._c_index >= self._index + self._visable:
                self._index += 1
            self._elements[self._c_index]._hover(self)
            self._update()

    def _up(self):
        if self._c_index > 0:
            self._elements[self._c_index]._dehover(self)
            self._c_index -= 1
            if self._c_index < self._index:
                self._index -= 1
            self._elements[self._c_index]._hover(self)
            self._update()

    def _select(self):
        return self._elements[self._c_index]._select(self)

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Menu

    def press(self):
        self.window._up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Menu

    def press(self):
        self.window._down()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Menu

    def press(self):
        self.window._select()

class MenuSingle(core.render.Window):

    template = core.asset.Template("std::menu", path="menu.template")

    def __init__(self, **items):
        items["Return"] = self.finish
        self.menu_elements = [(core.element.Text(core.Vector(3, 32), f'{text[:20]}>', size=11, justify="L", colour=1), func) for text, func in items.items()]
        self.down_arrow, self.up_arrow = core.element.Text(core.Vector(64, 50), '\\/'), core.element.Text(core.Vector(64, 14), '/\\')
        self.index = 0

    def render(self):
        self.menu_elements[self.index][0].render()
        if self.index > 0:
            self.up_arrow.render()
        if self.index < len(self.menu_elements)-1:
            self.down_arrow.render()

    def up(self):
        if self.index > 0:
            self.index -= 1

    def down(self):
        if self.index < len(self.menu_elements)-1:
            self.index += 1

    @core.render.Window.focus
    def select(self):
        command =  self.menu_elements[self.index][1]
        if command is None:
            pass
        elif isinstance(command, core.render.Window):
            res = yield command
            return res
        else:
            return command()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = MenuSingle

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = MenuSingle

    def press(self):
        self.window.down()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = MenuSingle

    def press(self):
        self.window.select()
