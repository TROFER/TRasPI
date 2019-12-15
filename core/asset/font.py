from core.asset.asset import Asset
from core.vector import Vector
import PIL.ImageFont

__all__ = ["Font"]

class _Font(Asset):

    def __call__(cls, name, size=None, new=False, **kwargs):
        # print(cls, name, size, new, kwargs)
        if size is not None:
            return super().__call__(name, size, new=True, **kwargs)
        return super().__call__(name, **kwargs)

class Font(metaclass=_Font):

    def __init__(self, size: int):
        self._size = size
        self._compute_font()

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = value
        self._compute_font()

    @property
    def font(self):
        return self._font

    def font_size(self, text) -> int:
        return Vector(*self._font.getsize(text))

    def _compute_font(self):
        self._font = PIL.ImageFont.truetype(self._path, self._size)
        return self._font
