import core


class Backlight:

    def __init__(self, colours: list, speed: float):
        self.active_colours = []
        self.colours = colours
        self.speed = speed
        self.x = 0

    def render(self, frame):
        self.active_colours = [self.colours[i]
                               for i in range(self.x, self.x + 128, 22)]
        core.hw.Backlight.gradient(self.active_colours, hsv=False, force=True)
        return frame

    def increment(self):
        if self.x + self.speed < len(self.colours) - 1:
            self.x += self.speed

    def decrement(self):
        if self.x - self.speed > 0:
            self.x -= self.speed

class AnimatedBacklight:

    def __init__(self, colours: list, speed: float):
        self.colours = colours
        self.index = 0
        self.active_colour = self.colours[self.index]
    
    def render(self, frame):
        core.hw.Backlight.fill(self.colours[self.index], hsv=False, force=True)

