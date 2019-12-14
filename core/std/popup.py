import core

class Error(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/error.template"

    def __init__(self, message):
        self.message = core.render.element.Text(core.Vector(124, 27), message, size=10, justify="R")

    def render(self):
        self.message.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Error

    def press(self):
        self.window.finish()

class Warning(Error):
  template = f"{core.sys.PATH}core/asset/template/warning.template"

class Info(Error):
    template = f"{core.sys.PATH}core/asset/template/info.template"
