import core

__all__ = ["Query"]

class Query(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/query.template"

    def __init__(self, message, title="Query", cancel=False):
        self.message = core.render.element.Text(core.Vector(64, 16), message) #FONT: 10
        self.selection = True
        self.cancel = core.render.element.Text(core.Vector(64, 16), "To Cancel Press 'Return'", size=11) if cancel else None #FONT: 8

    def render(self):
        self.message.render()
        if self.cancel is not None:
            self.cancel.render()

    def select_left(self):
        self.selection = True

    def select_right(self):
        self.selection = False

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Query

    def press(self):
        self.window.select_left()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Query

    def press(self):
        self.window.select_right()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Query

    def press(self):
        self.window.finish(Query.selection)
        # Because self <type: Handle> has no attribute 'selection'
        # 'selection' is an attribute of <type: Query>
        # How do we access member variables of a window when within the handler?

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Query

    def press(self):
        self.window.finish()
