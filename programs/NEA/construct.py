import random
from time import sleep

import yaml
from PIL import Image, ImageDraw

from library import library as lib
from misc import CD, align


class Segment:

    def __init__(self, theme_id, end):
        self.base = Base(theme_id, end=end)
        self.background = Background(theme_id)
        self.foreground = Foreground(theme_id, end=end)

    def get_asset(self, type_id, theme_id):
        lib.c.execute("SELECT image_id FROM asset WHERE type_id = ? AND theme_id = ?",
                      [type_id, theme_id])
        image_id = random.choice(lib.c.fetchall())[0]
        lib.c.execute("SELECT data, width, height FROM image WHERE id = ?",
                      [image_id])
        image = lib.c.fetchone()
        return Image.frombytes("RGBA", (image[1], image[2]), image[0])

    def randomise_positions(self, positions):
        output = []
        iterations = random.randint(1, len(positions) - 1)
        while iterations != 0:
            choice = random.choice(positions)
            positions.remove(choice)
            output.append(choice)
            iterations -= 1
        return output


class Base(Segment):

    def __init__(self, theme_id, end=False):
        self.theme_id = theme_id
        self.image = Image.new("RGBA", (128, 65), color=(255, 255, 255))
        self.type_id = lib.get_typeid("base", end=int(end))
        self.image.alpha_composite(self.get_asset(self.type_id, theme_id))
        self.draw_palette()

    def draw_palette(self):
        image_draw = ImageDraw.Draw(self.image)
        type_id = lib.get_typeid("palette")
        theme_palette = [colour for colour in self.get_asset(
            type_id, self.theme_id).getdata()]
        for x in range(21, 149, 21):
            image_draw.line([(x - 21, 64), (x, 64)],
                            fill=random.choice(theme_palette))


class Background(Segment):

    Furniture = {"x": [64, 32], "y": 53}
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
        return True if x1 > x2 and y1 > y2 else False


class Foreground(Background, Segment):

    Furniture = {"x": [32, 64, 96], "y": 53}

    def __init__(self, theme_id, end=False):
        self.theme_id = theme_id
        self.type_id = lib.get_typeid("foreground", end=int(end))
        self.image = self.get_asset(self.type_id, self.theme_id)
        super().place_furniture()

    def check_size(self, x1, y1, x2, y2):
        return True if x1 < x2 and y1 < y2 else False
