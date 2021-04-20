import core
from app import App
from core import Vector
from core.render.element import Image, Text

from game import library, keyboard


class Main(core.render.Window):
    
    def __init__(self):
        self.sprites = self.load_sprites()
        self.index = 0
        self.current_sprite = self.sprites[self.index]

        # Elements 

        self.title = Text(Vector(64, 3), "Select a player skin")
        self.sprite = Image(Vector(64, 32), self.current_sprite, just_h="C")
        self.index_label = Text(Vector(64, 50), self.index)
    
        self.elements = [self.title, self.sprite, self.index_label]
    
    async def show(self):
        # Bind Hotkeys

        keyboard.Hotkey("e", self.select)
        keyboard.Hotkey("a", self.left)
        keyboard.Hotkey("d", self.right)
    
    def load_sprites(self):
        type_id = library.lib.fetch_typeid("texture", "player-skin")
        library.lib.databases["textures"].c.execute(
            "SELECT image_id FROM texture WHERE type_id = ?", [type_id])
        image_ids = [_id[0] for _id in library.lib.databases["textures"].c.fetchall()]
        sprites = []
        for image_id in image_ids:
            sprites.append(library.lib.fetch_image(image_id))
        return sprites

    def render(self):
        for element in self.elements:
            core.Interface.render(element)
        


        