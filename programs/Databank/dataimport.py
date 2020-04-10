import core
import threading
import json


class Main(core.render.Window):

    core.hardware.Backlight.fill(10, 114, 211)

    def __init__(self):
        pass

    def render(self):
        pass
        
    @core.render.Window.focus
    def show(self):
        super().show()
        encrypt = yield core.std.Query(title="Encryption", message="Encrypt Data?")
        if encrypt:
            with open(f'{core.sys.PATH}programs/Databank/index.json', 'r') as index:
                self.methods = json.load(index)[0]
            self.encryption = yield core.std.MenuSingle(**self.methods)
        else:
            self.encryption = None
        compress = yield core.std.Query(title="Compression", message="Compress Data?")
        if compress:
            with open(f'{core.sys.PATH}programs/Databank/index.json', 'r') as index:
                self.methods = json.load(index)[1]
            self.compression = yield core.std.MenuSingle(**self.methods)
        else:
            self.compression = None
        yield Execute(self.encryption, self.compression)

class Execute(core.render.Window):

    template = core.asset.template("std::window")

    def __init__(self, encryption, compression):
        self.elements = [
            core.element.Text(
                core.Vector(3, 5), "Importer", justify="L"),
            core.element.Text(
                core.Vector(64, 20), "Status: Waiting"),
            core.element.Text(
                core.Vector(45, 32), "Loading..."),
            core.element.Line(core.Vector(3, 50), core.Vector(125, 50), width=3)]
    
    def render(self):
        for element in self.elements:
            element.render()
    
    def show(self):
        pass
        


