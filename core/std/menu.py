import core

__all__ = ["Menu", "MenuSingle"]

'''class Item:

    def __init__(self, name: str, image: str, path: str):
        self.icon = core.element.Image(core.Vector(0, 0), core.asset.Image(image))
        self.label = core.element.Text(core.Vector(0, 0), name, justify="L")
        self.name = name
        self.path = path

    def select(self):
        pass

    def render(self, index):
        self.icon.pos = core.Vector(5, 20 + 10 * index)
        self.icon.render()
        self.label.pos = core.Vector(12, 20 + 10 * index)
        self.label.render()
'''

class MenuElement:

    def __init__(self, *element: core.element, data={}, select=lambda self: None, hover=None, dehover=None):
        self.data = data
        self.elements = element
        self._rel_pos = [elm.pos for elm in self.elements]
        self._offset = 1
        self._index = -1
        self._select = select
        self._hover = hover
        self._dehover = dehover

    def _update(self, index):
        if index != self._index:
            self._index = index
            for i, elm in enumerate(self.elements):
                elm.pos = self._rel_pos[i] + core.Vector(2, 12 + self._offset * self._index)

    def render(self):
        for elm in self.elements:
            elm.render()

    def select(self, window):
        self._select(self, window)

    def hover(self):
        pass

    def dehover(self):
        pass

class Menu(core.render.Window):

    Element = MenuElement
    template = core.asset.Template("std::window", path="window.template")

    def __init__(self, *items: MenuElement, visable=4, offset=10):
        self.visable = visable
        self.items = list(items)
        self.items.append(MenuElement(core.element.Text(core.Vector(0, 0), "Return", justify="L"), select=lambda s, w: w.finish()))
        for elm in self.items:
            elm._offset = offset
        self.c_items = []

        self.index = 0
        self.c_index = self.index
        self._update()

    def render(self):
        for elm in self.c_items:
            elm.render()

    def _update(self):
        self.c_items.clear()
        for index, elm in enumerate(self.items[self.index:self.index + self.visable]):
            self.c_items.append(elm)
            elm._update(index)

    def down(self):
        if self.c_index < len(self.items) - 1:
            self.items[self.c_index].dehover()
            self.c_index += 1
            if self.c_index >= self.index + self.visable:
                self.index += 1
            self.items[self.c_index].hover()
            self._update()

    def up(self):
        if self.c_index > 0:
            self.items[self.c_index].dehover()
            self.c_index -= 1
            if self.c_index < self.index:
                self.index -= 1
            self.items[self.c_index].hover()
            self._update()

    def select(self):
        return self.items[self.c_index].select(self)

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Menu

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Menu

    def press(self):
        self.window.down()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Menu

    def press(self):
        self.window.select()

class MenuSingle(core.render.Window):

    template = core.asset.Template("std::menu", path="menu.template")

    def __init__(self, **items):
        items["Return"] = self.finish
        self.menu_items = [(core.element.Text(core.Vector(3, 32), f'{text[:20]}>', size=11, justify="L", colour=1), func) for text, func in items.items()]
        self.down_arrow, self.up_arrow = core.element.Text(core.Vector(64, 50), '\\/'), core.element.Text(core.Vector(64, 14), '/\\')
        self.index = 0

    def render(self):
        self.menu_items[self.index][0].render()
        if self.index > 0:
            self.up_arrow.render()
        if self.index < len(self.menu_items)-1:
            self.down_arrow.render()

    def up(self):
        if self.index > 0:
            self.index -= 1

    def down(self):
        if self.index < len(self.menu_items)-1:
            self.index += 1

    @core.render.Window.focus
    def select(self):
        command =  self.menu_items[self.index][1]
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
