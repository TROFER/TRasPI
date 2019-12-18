from core.asset.asset import Asset
import PIL.Image

__all__ = ["Template"]

class Template(metaclass=Asset):

    def __init__(self):
        self._image = PIL.Image.open(self._path).convert("P")

    def __repr__(self) -> str:
        return "<Asset: {}[{}] {} : {}>".format(self.__class__.__name__, self._name, self._path, self._image)

    @property
    def image(self):
        return self._image

    def copy(self):
        return self._image.copy()
