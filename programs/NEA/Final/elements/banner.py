import core

class Banner(core.render.Primative):

    def __init__(self, pos, text="Default Text"):
        self.text = text
        self.pos = pos
