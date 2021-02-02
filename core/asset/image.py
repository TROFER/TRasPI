from core.asset.base import Asset
import PIL.Image
from core.vector import Vector

__all__ = ["Image", "Template", "Icon"]

class Image(Asset):

    def __init__(self, path: str):
        if isinstance(path, PIL.Image.Image):
            self.path = ""
            self.image = path
        else:
            self.path = path
            self.image = PIL.Image.open(self.path).convert("1")

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
