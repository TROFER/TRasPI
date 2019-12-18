import core

__all__ = ["Info", "Warning", "Error"]

class Info(core.render.Window):

    template = core.asset.Template("std::info", path="info.template")

    def __init__(self, message):
        self.message = core.render.element.Text(core.Vector(38, 27), f'{message[:20]}', size=11, justify="L")#Font Was 8

    def render(self):
        self.message.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Info

    def press(self):
        self.window.finish()

class Warning(Info):
  template = core.asset.Template("std::warning", path="info.template")

class Error(Info):
    template = core.asset.Template("std::error", path="info.template")
