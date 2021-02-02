import random

from PIL import Image, ImageDraw

from library import library as lib
from misc import align


class Room:

    Constraints = {"min": 2, "max": 5}

    def __init__(self):
        lib.c.execute("SELECT id FROM theme")
        self.theme_id = random.choice(lib.c.fetchall())[0]
        self.x, self.y = random.randint(
            self.Constraints["min"], self.Constraints["max"]) * 128, 64
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
        self.lighting = Image.new("RGBA", (self.x, self.y), color=0)
        multiplier = 32
        type_id = lib.get_typeid("fixing")
        for x in range(multiplier, self.x, multiplier):
            image = self.get_asset(type_id, self.theme_id)
            x, y = x + align(image, "x", "C"), self.Fixing["y"]
            self.lighting.alpha_composite(image, (x, y))


class Base:

    def __init__(self, theme_id):
        self.theme_id = theme_id
        self.image = Image.new("RGBA", (128, 65), color=(255, 255, 255))
        self.type_id = lib.get_typeid("base")
        self.image.alpha_composite(self.get_asset(self.type_id, theme_id))
        self.draw_palette()

    def draw_palette(self):
        image_draw = ImageDraw.Draw(self.image)
        type_id = lib.get_typeid("palette")
        theme_palette = [colour for colour in self.get_asset(
            type_id, self.theme_id).getdata()]
        for x in range(21, 150, 22):
            image_draw.line([(x - 21, 64), (x, 64)],
                            fill=random.choice(theme_palette))

    def randomise_positions(self, positions):
        output = []
        iterations = random.randint(1, len(positions) - 1)
        while iterations != 0:
            choice = random.choice(positions)
            positions.remove(choice)
            output.append(choice)
            iterations -= 1
        return output

    def get_asset(self, type_id, theme_id):
        lib.c.execute("SELECT image_id FROM asset WHERE type_id = ? AND theme_id = ?",
                      [type_id, theme_id])
        image_id = random.choice(lib.c.fetchall())[0]
        lib.c.execute("SELECT data, width, height FROM image WHERE id = ?",
                      [image_id])
        image = lib.c.fetchone()
        return Image.frombytes("RGBA", (image[1], image[2]), image[0])


class Background(Base):

    Furniture = {"x": [42, 84], "y": 42}
    Contraints = [25, 25]

    def __init__(self, theme_id):
        self.theme_id = theme_id
        self.type_id = lib.get_typeid("background")
        self.image = self.get_asset(self.type_id, self.theme_id)
        self.place_furniture()

    def place_furniture(self):
        type_id = lib.get_typeid("furniture")
        lib.c.execute("SELECT image_id FROM asset WHERE type_id = ? AND theme_id = ?", [
                      type_id, self.theme_id])
        pool = []
        for image_id in [res[0] for res in lib.c.fetchall()]:
            lib.c.execute(
                "SELECT width, height, data FROM image WHERE id = ?", [image_id])
            asset = lib.c.fetchone()
            if self.check_size(asset[0], asset[1], *self.Contraints):
                pool.append(Image.frombytes(
                    "RGBA", (asset[0], asset[1]), asset[2]))
        for x in self.randomise_positions(self.Furniture["x"].copy()):
            image = random.choice(pool)
            x, y = x + align(image, "x",
                             'C'), self.Furniture["y"] + align(image, "y", "B")
            self.image.alpha_composite(image, (x, y))

    def check_size(self, x1, y1, x2, y2):
        return True if x1 >= x2 or y1 >= y2 else False


class Foreground(Background, Base):

    Furniture = {"x": [32, 64, 96], "y": 53}

    def __init__(self, theme_id, end=False):
        self.theme_id = theme_id
        self.type_id = lib.get_typeid("foreground", end=int(end))
        self.image = self.get_asset(self.type_id, self.theme_id)
        super().place_furniture()

    def check_size(self, x1, y1, x2, y2):
        return True if x1 <= x2 and y1 <= y2 else False