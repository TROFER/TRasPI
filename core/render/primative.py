import PIL.ImageDraw

__all__ = ["Primative"]

class Primative:

    def __init__(self):
        self._widget = (self,)
    def __repr__(self):
        pass

    def render(self, image: PIL.ImageDraw.ImageDraw):
        raise TypeError("Needs Render Function")

    def copy(self):
        raise TypeError("Needs copy Constructor")

    def volatile(self):
        return False

class Test:

    def __init__(self, text):
        self.text = text

    def render(self, image: PIL.ImageDraw.ImageDraw):
        image.text((0, 0), self.text, fill=1)