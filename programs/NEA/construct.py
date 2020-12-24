from library import library as lib
from PIL import Image
import random
import yaml

class Segment:

    ELEMENTS = lib.ASSET_TYPES


    def __init__(self, theme_id, end=None):
        self.end = end
        self.theme_id = theme_id
        self.foreground, self.background, self.base = self.generate()

    def generate(self):
        fg = Image.new("RGBA", (128, 64), 0)
        lib.c.execute("SELECT id FROM type WHERE name = ? AND end = ?", ["foreground", int(self.end)])
        fg.alpha_composite(self.pick_asset(lib.c.fetchone()[0]))
        lib.c.execute("SELECT id FROM type WHERE name = ?", ["furniture"])
        furniture_id = lib.c.fetchone()[0]
        for position in self.pick_positions('YAML CODE HERE'):
            fg.alpha_composite(self.pick_asset(furniture_id))
    
    def pick_positions(self, positions):
        res = []
        for i in range(random.randint(0, len(positions) - 1)):
            choice = random.choice(positions)        
            positions.pop(choice)
            res.append(choice)
        return res
    
    def pick_asset(self, type_id):
        lib.c.execute("SELECT image_id FROM asset WHERE type_id = ? AND theme_id = ?", [type_id, self.theme_id])
        image_id = random.choice(lib.c.fetchall())[0]
        lib.c.execute("SELECT data, width, height FROM image WHERE id = ?", [image_id])
        data = lib.c.fetchone()
        return Image.frombytes("RGBA", (data[1], data[2]), data[0])

        

Segment(1)

    
# ADD SIZE BASED SELECTION