import random

from game.library import lib
from PIL import Image as PIL

from generation.common import align
from generation.layers import Background, Base, Fixings, Foreground


class Room:

    def __init__(self, width):
        # Set ids
        type_id = lib.fetch_typeid("pack", "room")
        lib.c.execute("SELECT id FROM pack WHERE type = ? ", [type_id])
        self.pack_id = random.choice(lib.c.fetchall())[0]
        # Generate
        self.x, self.y = width * 128, 64
        self.generate_base(), self.generate_background(), self.generate_foreground()
        self.generate_fixings()

    def generate_base(self):
        self.base = PIL.new("RGBA", (self.x, 65), color=0)
        for x in range(0, self.x, 128):
            self.base.alpha_composite(Base(self.pack_id).image, (x, 0))

    def generate_background(self):
        self.background = PIL.new("RGBA", (self.x, self.y), color=0)
        for x in range(0, self.x, 128):
            self.background.alpha_composite(
                Background(self.pack_id).image, (x, 0))

    def generate_foreground(self):
        self.foreground = PIL.new("RGBA", (self.x, self.y), color=0)
        self.foreground.alpha_composite(Foreground(
            self.pack_id, end=True).image, (0, 0))
        self.foreground.alpha_composite(Foreground(self.pack_id, end=True).image.transpose(
            PIL.FLIP_LEFT_RIGHT), (self.x - 128, 0))
        for x in range(128, self.x - 128, 128):
            self.foreground.alpha_composite(
                Foreground(self.pack_id).image, (x, 0))

    def generate_fixings(self):
        self.fixings = Fixings((self.x, self.y), self.pack_id).image


class Transition:

    Anchor = {
        "left": (32, 50),
        "center": (64, 50),
        "right": (95, 50)
    }

    def __init__(self, exits: tuple):
        self.exits = exits
        # Set ids
        lib.databases["textures"].c.execute("SELECT id FROM pack WHERE type_id = ?",
                                          [lib.fetch_typeid("pack", "transition")])
        self.pack_id = random.choice(lib.databases.c.fetchall())[0]
        # Construct
        self.load_frames()
        self.background = self.background_frames[0]
        self.foreground = self.foreground_frames[0]
        self.generate_exits()

    def load_frames(self):
        # Background Frames
        type_id = lib.fetch_typeid("texture", "background")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                          [self.pack_id, type_id])
        self.background_frames = []
        for image_id in lib.databases["textures"].c.fetchall():
            self.background_frames += lib.fetch_image(image_id[0])
        # Foregroud Frames
        type_id = lib.fetch_typeid("texture", "foreground")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?"
                                          [self.pack_id, type_id])
        self.foreground_frames = []
        for image_id in lib.databases["textures"].c.fetchall():
            self.foreground_frames += lib.fetch_image(image_id[0])

    def generate_exits(self):
        for build, name, anchor in zip(self.exits, ["left-exit", "center-exit", "right_exit"], self.Anchor.items()):
            if build:
                type_id = lib.fetch_typeid("texture", name)
                lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                                  [self.pack_id, type_id])
                image = lib.fetch_image(random.choice(
                    lib.databases["textures"].c.fetchall())[0])
                self.background.alpha_composite(image, anchor)
