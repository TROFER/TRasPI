import PIL.ImageDraw

__all__ = ["Primative"]

class Primative:

    zindex = 0

    def __init__(self, zindex: int=None):
        if zindex is not None:
            self.zindex = zindex
        self._widget = (self,)
    def __repr__(self) -> str:
        return f"Primative[{self.__class__.__name__}]"

    def render(self, image: PIL.ImageDraw.ImageDraw):
        """Given the ImageDraw obj to draw onto"""
        raise TypeError("Needs Render Function")

    def copy(self) -> tuple:
        """A tuple of Data required to identify it as unique"""
        raise TypeError("Needs copy Constructor")

    def volatile(self):
        """Run when the Primative needs updating"""
        return False
