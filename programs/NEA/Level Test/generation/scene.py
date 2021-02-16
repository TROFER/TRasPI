import random

from PIL import Image
from layers import Base, Background, Foreground, Fixings


class Room:

    def __init__(self, width):
        lib.c.execute("SELECT id FROM theme")
        self.theme_id = random.choice(lib.c.fetchall())[0]
        self.x, self.y = width * 128, 64
        self.generate_base(), self.generate_background(), self.generate_foreground()
        self.generate_fixings()

    def generate_base(self):
        self.base = Image.new("RGBA", (self.x, 65), color=0)
        for x in range(0, self.x, 128):
            self.base.alpha_composite(Base(self.theme_id).image, (x, 0))
    
    def generate_background(self):
        self.background = Image.new("RGBA", (self.x, self.y), color=0)
        for x in range(0, self.x, 128):
            self.background.alpha_composite(Background(self.theme_id).image, (x, 0))
    
    def generate_foreground(self):
        self.foreground = Image.new("RGBA", (self.x, self.y), color=0)
        self.foreground.alpha_composite(Foreground(self.theme_id, end=True).image, (0, 0))
        self.foreground.alpha_composite(Foreground(self.theme_id, end=True).image.transpose(
            Image.FLIP_LEFT_RIGHT), (self.x - 128, 0))
        for x in range(128, self.x - 128, 128):
            self.foreground.alpha_composite(Foreground(self.theme_id).image, (x, 0))
    
    def generate_fixings(self):
        self.fixings = Fixings((self.x, self.y), self.theme_id).image


class Transition:

    def __init__(self, type: tuple):
        self.image = Image.new("RGBA", (128, 64))


