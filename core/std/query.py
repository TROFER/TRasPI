import core

__all__ = ["Query"]

class Query(core.render.Window):

    template = core.asset.Template("std::query", path="query.template")

    def __init__(self, message, title="Query", cancel=False):
        self.message = core.element.Text(core.Vector(38, 27), message[:14], justify="L")
        self.title = core.element.Text(core.Vector(5, 5), title, justify="L")
        if cancel:
            bttn_yes = core.Vector(32, 56)
            bttn_no = core.Vector(64, 56)
            self.bttn_cancel = core.element.TextBox(core.Vector(96, 56), "Cancel")
        else:
            bttn_yes = core.Vector(31, 56)
            bttn_no = core.Vector(92, 56)
            self.bttn_cancel = None
        self.bttn_yes = core.element.TextBox(bttn_yes, "Yes")
        self.bttn_no = core.element.TextBox(bttn_no, "No")

    def render(self):
        self.message.render()
        self.title.render()
        self.bttn_no.render(), self.bttn_yes.render()
        if self.bttn_cancel is not None:
            self.bttn_cancel.render()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Query

    def press(self):
        self.window.finish(True)

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Query

    def press(self):
        self.window.finish(False)

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Query

    def press(self):
        self.window.finish(None)
