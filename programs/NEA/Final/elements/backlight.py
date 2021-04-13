from core.hw import Backlight


class Backlight(core.render.Primative):

    def __init__(self, colours: list, speed=float 5):
        super().__init__()
        self.active_colours = []
        self.colours = colours
        self.speed = speed
        self.x = 0

    def render(self, draw):
        self.active_colours = [self.colours[i]
                               for i in range(self.x, self.x + 128, 22)]
        Backlight.gradient(self.active_colours, hsv=False, force=True)

    def copy(self):
        return self.active_colours, self.x
    
    def increment(self):
        if self.x + self.speed >= len(self.colours) - 1:
            self.x += self.speed
    
    def decrement(self):
        if self.x - self.speed > 0:
            self.x -= self.speed
    
