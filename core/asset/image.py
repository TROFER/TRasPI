from core.asset.base import Asset
import PIL.Image
from core.vector import Vector

__all__ = ["Image", "Template", "Icon"]

class Image(Asset):

    def __init__(self, path: str, alpha=False):
        if isinstance(path, PIL.Image.Image):
            self.path = ""
            img: PIL.Image.Image = path.convert("LA")
        else:
            super().__init__(path)
            img: PIL.Image.Image = PIL.Image.open(self.path).convert("LA")
        self.image: PIL.Image.Image = img.getchannel(0)
        self.alpha: PIL.Image.Image = img.getchannel(1) if alpha else None

    def __repr__(self) -> str:
        return f"{super().__repr__()}<{self.image} {self.path}>"

    def copy(self) -> PIL.Image.Image:
        return self.image.copy()

    def size(self) -> Vector:
        return Vector(self.image.width, self.image.height)

class Template(Image):
    pass

class Icon(Image):
    pass
