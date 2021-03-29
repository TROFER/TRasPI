import random

from PIL import Image as PIL

from generation.common import align
from generation.layers import Background, Base, Fixings, Foreground
from game.library import library as lib


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

    ExitGeometryX = [32, 64, 95]
    ExitGeometryY = 50

    def __init__(self, _type: tuple):
        self.type = _type
        lib.c.execute("SELECT id FROM transition")
        self.transition_id = random.choice(lib.c.fetchall())[0]
        self.background, self.foreground = self.load_frames()
        self.generate_exits()

    def load_frames(self):
        self.bg_frames, self.fg_frames = [], []
        # Load Background Frames
        lib.c.execute("SELECT image_id FROM frame WHERE transition_id = ? AND type = ?", [self.transition_id, "bg"])
        self.bg_frames += [lib.fetch_image(_id[0]) for _id in lib.c.fetchall()]
        # Load Foreground Frames
        lib.c.execute("SELECT image_id FROM frame WHERE transition_id = ? AND type = ?", [self.transition_id, "fg"])
        self.fg_frames += [lib.fetch_image(_id[0]) for _id in lib.c.fetchall()]
        return self.bg_frames[0], self.fg_frames[0]

    def generate_exits(self):
        self.stage = PIL.new("RGBA", (128, 64))
        lib.c.execute("SELECT center_exit, left_exit, right_exit FROM transition WHERE id = ?", [self.transition_id])
        for _generate, x, image_id in zip(self.type, self.ExitGeometryX, lib.c.fetchone()):
            if _generate:
                image = lib.fetch_image(image_id)
                x += align(image, "x", "C")
                y = self.ExitGeometryY + align(image, "y", "B")
                self.stage.alpha_composite(image, dest=(x, y))

'''trs = Transition([True, False, True])
trs.background.alpha_composite(trs.stage)
trs.background.alpha_composite(trs.foreground)
trs.background.save("debug.png")
'''
