import random

from PIL import Image
from layers import Base, Background, Foreground, Fixings
from library import library as lib


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

    Destinations = {
        "top" : (25, 0, 103, 49),
        "bottom" : (25, 49, 103, 64),
        "right" : (103, 0, 128, 64),
        "left" : (0, 0, 25, 64)
    }

    Sources = {
        "top" : (153, 0, 231, 49),
        "bottom" : (153, 49, 231, 64),
        "right" : (231, 0, 256, 64),
        "left" : (128, 0, 153, 64)
    }

    def __init__(self, _type: tuple):
        """Generates a transition room"""
        self.image = Image.new("RGBA", (128, 64))
        self.generate(_type)
    
    def generate(self, _type):
        source = self.get_transition()
        self.image.paste(source.copy().crop((0, 0, 128, 64)), (0, 0))
        if _type[0]:
            image = source.copy().crop(self.Sources["top"])
            self.image.paste(image, self.Destinations["top"])
        if _type[1]:
            image = source.copy().crop(self.Sources["bottom"])
            self.image.paste(image, self.Destinations["bottom"])
        if _type[2]:
            image = source.copy().crop(self.Sources["right"])
            self.image.paste(image, self.Destinations["right"])
        if _type[3]:
            image = source.copy().crop(self.Sources["left"])
            self.image.paste(image, self.Destinations["left"])
    
    def get_transition(self):
        type_id = lib.get_typeid("transition")
        lib.c.execute("SELECT image_id FROM asset WHERE type_id = ?", [type_id])
        image_id = random.choice(lib.c.fetchall())[0]
        lib.c.execute("SELECT data, width, height FROM image WHERE id = ?", [image_id])
        image = lib.c.fetchone()
        return Image.frombytes("RGBA", (image[1], image[2]), image[0])

t = Transition((True, False, True, False))
t.image.save("D:/Documents/Programing/Python/TrasPi Operating System/programs/NEA/Level Test/output.png")