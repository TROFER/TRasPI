import core

__all__ = ["Menu"]

class Menu(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/menu.template"

    def __init__(self, **items):
        items["Return"] = self.window.finish
        self.menu_items = [(core.render.element.Text(core.Vector(3, 32), f'{text[:20]}>', size=11, justify="L", colour=0), func) for text, func in items.items()]
        self.down_arrow, self.up_arrow = core.render.element.Text(core.Vector(64, 50), '\\/'), core.render.element.Text(core.Vector(64, 14), '/\\')
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
