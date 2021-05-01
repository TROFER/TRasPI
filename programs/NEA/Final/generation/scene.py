import random

from game.library import lib
from PIL import Image as PIL

from generation.common import align
from generation.layers import Background, Base, Fixings, Foreground


class Scene:

    def __init__(self, packtype: str):
        type_id = lib.fetch_typeid("pack", packtype)
        lib.databases["textures"].c.execute(
            "SELECT id FROM pack WHERE type_id = ? ", [type_id])
        self.pack_id = random.choice(lib.databases["textures"].c.fetchall())[0]


class Animated(Scene):

    def load_frames(self):
        # Background Frames
        type_id = lib.fetch_typeid("texture", "background")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                            [self.pack_id, type_id])
        self.background_frames = []
        for image_id in lib.databases["textures"].c.fetchall():
            self.background_frames.append(lib.fetch_image(image_id[0]))

        # Foregroud Frames
        type_id = lib.fetch_typeid("texture", "foreground")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                            [self.pack_id, type_id])
        self.foreground_frames = []
        for image_id in lib.databases["textures"].c.fetchall():
            self.foreground_frames.append(lib.fetch_image(image_id[0]))

        # Backlight Colours
        type_id = lib.fetch_typeid("texture", "palette")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                            [self.pack_id, type_id])
        image = lib.fetch_image(
            lib.databases["textures"].c.fetchone()[0]).convert("RGB")
        self.backlight_colours = [colour for colour in image.getdata()]


class Room(Scene):

    def __init__(self, width):
        super().__init__("room")

        # Generate
        self.x, self.y = width * 128, 64
        self.generate_base(), self.generate_background(), self.generate_foreground()
        self.generate_fixings()

    def generate_base(self):
        # Create a blank image
        self.base = PIL.new("RGBA", (self.x, 65), color=0)
        # Fill in
        for x in range(0, self.x, 128):
            self.base.alpha_composite(Base(self.pack_id).image, (x, 0))

    def generate_background(self):
        # Create a blank image
        self.background = PIL.new("RGBA", (self.x, self.y), color=0)

        # Fill in
        for x in range(0, self.x, 128):
            self.background.alpha_composite(
                Background(self.pack_id).image, (x, 0))

    def generate_foreground(self):
        # Create a blank image
        self.foreground = PIL.new("RGBA", (self.x, self.y), color=0)

        # Paste Room Ends
        self.foreground.alpha_composite(Foreground(
            self.pack_id, end=True).image, (0, 0))
        self.foreground.alpha_composite(Foreground(self.pack_id, end=True).image.transpose(
            PIL.FLIP_LEFT_RIGHT), (self.x - 128, 0))
        
        # Fill in 
        for x in range(128, self.x - 128, 128):
            self.foreground.alpha_composite(
                Foreground(self.pack_id).image, (x, 0))

    def generate_fixings(self):
        self.fixings = Fixings((self.x, self.y), self.pack_id).image


class Branch(Animated, Scene):

    Anchor = {
        "left": (32, 50),
        "center": (64, 50),
        "right": (95, 50)
    }

    def __init__(self, exits: tuple):
        self.exits = exits
        super().__init__("branch")

        # Construct
        super().load_frames()
        self.generate_exits()

    def generate_exits(self):
        for frame in self.background_frames:
            for build, name, anchor in zip(self.exits, ["left-exit", "center-exit", "right-exit"], self.Anchor.values()):
                if build:
                    type_id = lib.fetch_typeid("texture", name)
                    lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                                        [self.pack_id, type_id])
                    image = lib.fetch_image(random.choice(
                        lib.databases["textures"].c.fetchall())[0])
                    x = anchor[0] + align(image, "X", "C")
                    y = anchor[1] + align(image, "Y", "B")
                    frame.alpha_composite(image, dest=(x, y))


class Treasure(Animated, Scene):

    def __init__(self):
        super().__init__("room-treasure")

        # Construct
        super().load_frames()
