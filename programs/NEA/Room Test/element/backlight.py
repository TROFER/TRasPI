import core

class Backlight(core.render.Primative):

    Step = 21

    def __init__(self, colours: list):
        super().__init__()
        self.active_colours = []
        self.colours = colours
        self.x = 0
    

    def render(self, draw):
        self.active_colours = [self.colours[i] for i in range(self.x, self.x + 128, 22)]
        core.hw.Backlight.gradient(self.active_colours, hsv=False, force=True)
    

    def copy(self):
        return self.active_colours

