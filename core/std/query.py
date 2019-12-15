import core

__all__ = ["Query"]

class Query(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/query.template"

    def __init__(self, message, title="Query", cancel=False):
        self.message = core.render.element.Text(core.Vector(64, 16), message)
        self.title = core.render.element.Text(core.Vector(5, 5), title)
        if cancel:
            self.bttn_yes = core.render.element.Text(core.Vector(42, 56), "Yes")
            self.bttn_no = core.render.element.Text(core.Vector(84, 56), "No")
            self.bttn_cancel = core.render.element.Text(core.Vector(126, 56), "Cancel")
        else:
            self.cancel = None
            self.bttn_no = core.render.element.Text(core.Vector(31, 56), "No")
            self.bttn_cancel = core.render.element.Text(core.Vector(94, 56), "Cancel")

    def render(self):
        self.message.render()
        self.title.render()
        self.bttn_no.render(), self.bttn_yes.render()
        if self.cancel is not None:
            self.cancel.render()

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
