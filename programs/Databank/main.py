import core
import dataimport



class Main(core.render.Window):

    core.hardware.Backlight.fill(10, 114, 211)
    template = core.asset.Template("std::window")
    core.asset.Image(
        "import", path=f"{core.sys.PATH}programs/Databank/asset/import.icon")
    core.asset.Image(
        "export", path=f"{core.sys.PATH}programs/Databank/asset/export.icon")
    core.asset.Image(
        "view", path=f"{core.sys.PATH}programs/Databank/asset/view.icon")

    def __init__(self):
        self.index = 0
        self.buttons = [core.element.Image(core.Vector(25, 32), core.asset.Image("import")), core.element.Image(
            core.Vector(64, 32), core.asset.Image("export")), core.element.Image(core.Vector(103, 32), core.asset.Image("view"))]
        self.labels = [core.element.TextBox(core.Vector(25, 55), "Import", rect_colour=0), core.element.TextBox(
            core.Vector(64, 55), "Export", rect_colour=1), core.element.TextBox(core.Vector(103, 55), "View", rect_colour=1)]
        self.title = core.element.Text(
            core.Vector(3, 5), "Databank", justify="L")

    def render(self):
        for button in self.buttons: 
            button.render()
        for label in self.labels:
            label.render()
        self.title.render()

    @core.render.Window.focus
    def subwindow(self):
        #subwindows = [importer.Main, exporter.Main, viewer.Main]
        subwindows = [dataimport.Main]
        yield subwindows[self.index]()



class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Main

    def press(self):
        self.window.finish()


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Main

    def press(self):
        if self.window.index > 0:
            self.window.labels[self.window.index].rect.colour = 1
            self.window.index -= 1
            self.window.labels[self.window.index].rect.colour = 0


class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Main

    def press(self):
        if self.window.index < 2:
            self.window.labels[self.window.index].rect.colour = 1
            self.window.index += 1
            self.window.labels[self.window.index].rect.colour = 0


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Main

    def press(self):
        self.window.subwindow()

main = Main()
