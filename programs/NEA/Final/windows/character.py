import core
from app import App
from core import Vector
from core.asset.image import Image as AssetImage
from core.render.element import Image, Line, Text
from PIL import Image as PIL

from game import keyboard, library


class Main(core.render.Window):
    
    def __init__(self):
        super().__init__()
        self.sprites = self.load_sprites()
        self.index = 0
        self._flag = None

        # Elements 

        self.title = Text(Vector(64, 5), "Select Player Skin")
        self.sprite = Image(Vector(64, 32), self.sprites[self.index]["image"], just_h="C")
        self.index_label = Text(Vector(64, 57), f"{self.index + 1} / {len(self.sprites)}")
    
        self.elements = [self.title, self.sprite, self.index_label, 
            Line(Vector(0, 10), Vector(128, 10)),
            Line(Vector(0, 50), Vector(128, 50))]
        
        App.interval(self.check_flag, 0.1)
    
    async def show(self):
        # Reset
        self._flag = None
        keyboard.clear_all()

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
            image = AssetImage(remove_alpha(library.lib.fetch_image(image_id)))
            sprites.append(
                {"image" : image,
                 "id" : image_id})
        return sprites

    def render(self):
        for element in self.elements:
            core.Interface.render(element)
    
    def check_flag(self):
        if self._flag is not None:
            self._flag()
    
    def select(self):
        App.var.playerskin = self.sprites[self.index]["id"]
        self._flag = self.finish
    
    def right(self):
        self.index = (self.index + 1) % len(self.sprites)
        self._any()
    
    def left(self):
        self.index = (self.index - 1) % len(self.sprites)
        self._any()

    def _any(self):
        self.elements[1] = Image(Vector(64, 32), self.sprites[self.index]["image"], just_h="C")
        self.elements[2].text = f"{self.index + 1} / {len(self.sprites)}"

def remove_alpha(image):
    """Replaces image alpha with white pixels"""
    new = []
    for pixel in image.getdata():
        if pixel[3] == 0:
            new.append((255, 255, 255))
        else:
            new.append(pixel)
    image.putdata(new)
    return image

