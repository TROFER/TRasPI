from core.asset.base import Asset
import PIL.ImageFont
from core.vector import Vector

class Font(Asset):

    def __init__(self, path: str, size: int):
        self.__path_original = path
        super().__init__(path)
        self.size = size
        self.__calculate_font()

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.size == other.size
    def __ne__(self, other) -> bool:
        return super().__ne__(other) and self.size != other.size

    def __repr__(self) -> str:
        return f"{super().__repr__()}<{self.size} {self.font} {self.path}>"

    def resize(self, size: int) -> "Font":
        return self.__class__(self.__path_original, size)

    def text_pixel_size(self, text: str) -> Vector:
        return Vector(*self.font.getsize(text))

    def __calculate_font(self):
        self.font = PIL.ImageFont.truetype(self.path, self.size)