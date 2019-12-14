import core

__all__ = ["Menu"]

class Menu(core.render.Window):

    template = f"{core.sys.PATH}/asset/template/menu.template"

    def __init__(self, **items):
        self.menu_items = [(core.render.element.Text(core.Vector(3, 32), text, size=10, justify="L", colour=0), func) for text, func in items.items()]
        self.index = 0

    def render(self):
        self.menu_items[self.index][0].render()

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
