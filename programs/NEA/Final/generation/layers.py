import random

from game.library import lib
from PIL import Image, ImageDraw

from generation.common import align


class Base:

    def __init__(self, pack_id):
        # Set ids
        self.pack_id = pack_id
        self.type_id = lib.fetch_typeid("texture", "base")
        # Construct
        self.image = Image.new("RGBA", (128, 65), color=(255, 255, 255))
        self.image.alpha_composite(self.get_texture(self.pack_id, self.type_id))
        self.draw_palette()

    def draw_palette(self):
        image_draw = ImageDraw.Draw(self.image)
        type_id = lib.fetch_typeid("texture", "palette")
        theme_palette = [colour for colour in self.get_texture(
            self.pack_id, type_id).getdata()]
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

    def get_texture(self, pack_id, type_id):
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?",
                                          [pack_id, type_id])
        return lib.fetch_image(random.choice(lib.databases["textures"].c.fetchall())[0])


class Background(Base):

    Furniture = {"x": [42, 84], "y": 42}
    Contraints = [25, 25]

    def __init__(self, pack_id):
        # Set ids
        self.pack_id = pack_id
        self.type_id = lib.fetch_typeid("texture", "background")
        # Construct
        self.image = self.get_texture(self.pack_id, self.type_id)
        self.place_furniture()

    def place_furniture(self):
        type_id = lib.fetch_typeid("texture", "furniture")
        lib.databases["textures"].c.execute("SELECT image_id FROM texture WHERE pack_id = ? AND type_id = ?", [
            self.pack_id, type_id])
        pool = []
        for image_id in [res[0] for res in lib.databases["textures"].c.fetchall()]:
            lib.databases["textures"].c.execute(
                "SELECT width, height, data FROM image WHERE id = ?", [image_id])
            texture = lib.databases["textures"].c.fetchone()
            if self.check_size(texture[0], texture[1], *self.Contraints):
                pool.append(Image.frombytes(
                    "RGBA", (texture[0], texture[1]), texture[2]))
        for x in self.randomise_positions(self.Furniture["x"].copy()):
            image = random.choice(pool)
            x, y = x + align(image, "x",
                             'C'), self.Furniture["y"] + align(image, "y", "B")
            self.image.alpha_composite(image, (x, y))

    def check_size(self, x1, y1, x2, y2):
        return True if x1 >= x2 or y1 >= y2 else False


class Foreground(Background, Base):

    Furniture = {"x": [32, 64, 96], "y": 53}

    def __init__(self, pack_id, end=False):
        # Set ids
        self.pack_id = pack_id
        if end:
            self.type_id = lib.fetch_typeid("texture", "foreground-end")
        else:
            self.type_id = lib.fetch_typeid("foreground", "foreground")
        # Construct
        self.image = self.get_texture(self.pack_id, self.type_id)
        super().place_furniture()

    def check_size(self, x1, y1, x2, y2):
        return True if x1 <= x2 and y1 <= y2 else False


class Fixings(Base):

    Spacing = 32

    def __init__(self, size: tuple, pack_id):
        # Set ids
        self.pack_id = pack_id
        self.type_id = lib.fetch_typeid("texture", "fixing")
        # Construct
        self.image = Image.new("RGBA", size, color=0)
        for x in range(self.Spacing, size[0] - self.Spacing, self.Spacing):
            image = self.get_texture(self.pack_id, self.type_id)
            x, y = x + align(image, "x", "C"), 0
            self.image.alpha_composite(image, (x, y))
