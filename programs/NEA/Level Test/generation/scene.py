import random

from PIL import Image as PIL
from layers import Base, Background, Foreground, Fixings
from library import library as lib
from misc import align


class Room:

    def __init__(self, width):
        lib.c.execute("SELECT id FROM theme")
        self.theme_id = random.choice(lib.c.fetchall())[0]
        self.x, self.y = width * 128, 64
        self.generate_base(), self.generate_background(), self.generate_foreground()
        self.generate_fixings()

    def generate_base(self):
        self.base = PIL.new("RGBA", (self.x, 65), color=0)
        for x in range(0, self.x, 128):
            self.base.alpha_composite(Base(self.theme_id).image, (x, 0))

    def generate_background(self):
        self.background = PIL.new("RGBA", (self.x, self.y), color=0)
        for x in range(0, self.x, 128):
            self.background.alpha_composite(
                Background(self.theme_id).image, (x, 0))

    def generate_foreground(self):
        self.foreground = PIL.new("RGBA", (self.x, self.y), color=0)
        self.foreground.alpha_composite(Foreground(
            self.theme_id, end=True).image, (0, 0))
        self.foreground.alpha_composite(Foreground(self.theme_id, end=True).image.transpose(
            PIL.FLIP_LEFT_RIGHT), (self.x - 128, 0))
        for x in range(128, self.x - 128, 128):
            self.foreground.alpha_composite(
                Foreground(self.theme_id).image, (x, 0))

    def generate_fixings(self):
        self.fixings = Fixings((self.x, self.y), self.theme_id).image


class Transition:

    Anchors = [(64, 55), (64, 62), (15, 55), (113, 55)]

    def __init__(self, _type: tuple):
        self.type = _type
        lib.c.execute("SELECT id FROM transition")
        self.transition_id = random.choice(lib.c.fetchall())[0]
        self.load_frames(), self.generate_background

    def load_frames(self):
        lib.c.execute("SELECT image_id FROM frame WHERE transition_id = ?", [
                      self.transition_id])
        self.frames = []
        for image_id in lib.c.fetchall():
            lib.c.execute(
                "SELECT data, width, height FROM image WHERE id = ?", [image_id[0]])
            _image = lib.c.fetchone()
            self.frames.append(PIL.frombytes(
                "RGBA", (_image[1], _image[2]), _image[0]))
        self.background = self.frames[0]

    def generate_background(self):
        self.foreground = PIL.new("RGBA", (128, 64))
        lib.c.execute("SELECT north_exit, south_exit, left_exit, right_exit FROM transition WHERE id = ?", [
                      self.transition_id])
        for i, image_id in enumerate(lib.c.fetchone()):
            if self.type[i]:
                _image = lib.fetch_image(image_id)
                _anchor = (self.Anchors[i][0] + align(_image, "x", "C"), 
                            self.Anchors[i][1] + align(_image, "y", "B") if i != 0 else 0)
                self.foreground.paste(_image, (_anchor))

trs = Transition([True, True, True, True])