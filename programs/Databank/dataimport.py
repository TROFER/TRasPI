import core
import threading
import json
import time


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
        data = yield Execute(self.encryption, self.compression)
        save = core.std.Query(title="Importer", message="Save to documents?")
        if save:
            with open(f"{core.sys.PATH}user/documents/{time.stftime('%d.%m.%y %T')}.txt", 'w') as file:
                file.write(data)
        self.finish()


class Execute(core.render.Window):

    def constrain(self, n, start1, stop1, start2, stop2):
        return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

    template = core.asset.template("std::window")

    def __init__(self, encryption, compression):
        self.encryption, self.compression = encryption, compression
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
    
    async def show(self):
        with open(f"{core.sys.PATH}user/documents/input.txt", 'r') as file:
            self.data = file.read()
            if self.encryption is not None:
                parent = core.sys.io
                for i in self.encryption.split("."):
                    parent = getattr(parent, i)
                method = parent
                # Start Processing - returns key and data
                with open(f"{core.sys.PATH}user/documents/keys.txt", 'a') as file:
                    file.write(key)
        if self.compression is not None:
            parent = core.sys.io
            for i in self.compression.split("."):
                parent = getattr(parent, i)
            method = parent
            # Start Processing - returns data
        with open(f"{core.sys.PATH}user/documents/output.txt", 'w') as file:
            file.write(self.data)
        self.finish(self.data)

    def callback(self, value):
        self.elements[3].pos1 = Vector(contrain(value, 0, len(self.data), 3, 125 ), 50)

