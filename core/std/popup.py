import core

__all__ = ["Info", "Warning", "Error"]

class Info(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/info.template"

    def __init__(self, message):
        self.message = core.render.element.Text(core.Vector(124, 27), message, size=10, justify="L")

    def render(self):
        self.message.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Info

    def press(self):
        self.window.finish()

class Warning(Info):
  template = f"{core.sys.PATH}core/asset/template/warning.template"

class Error(Info):
    template = f"{core.sys.PATH}core/asset/template/error.template"
