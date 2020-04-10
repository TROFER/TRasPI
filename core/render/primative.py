import PIL.ImageDraw

__all__ = ["Primative"]

class Primative:

    def __init__(self):
        pass
    def __repr__(self):
        pass

    def render(self):
        return core.driver.pipeline.widget.Widget()

class Test:

    def __init__(self, text):
        self.text = text

    def render(self, image: PIL.ImageDraw.ImageDraw):
        image.text((0, 0), self.text, fill=1)