from core.vector import Vector
from core.render.enums import Button, Event
from core.render.handle import Handler
from core.render.screen import Screen
from core.render.renderer import Render
# import core.render.template

import PIL.Image

__all__ = ["Window", "Element"]

class MetaWindow(type):

    def __new__(cls, name, bases, attrs):
        attrs["_handles"] = [None] * 6
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        self = super().__call__(*args, **kwargs)
        self.elements = {}
        return self

class Window(metaclass=MetaWindow):

    _handles = [None] * 6
    template = Image.open(PATH+"core/assets/menu.template").convert("P")

    def __init__(self):
        self.elements = {}

    def render(self):
        pass

    def template(self, image: str):
        if isinstance(image, str):
            image = PIL.Image.open(image).convert("P")
        self._template = image

    def show(self):
        Screen().show(self)

    def finish(self, value=None):
        parent, generator = Screen().call_lost()
        parent.show()
        if generator is not None:
            parent._handle_focus(value, generator)
        return value

    def _handle_focus(self, value, generator):
        try:
            window = generator.send(value)
            if isinstance(window, Window):
                Screen().call_focus(generator, self)
                window.show()
        except StopIteration as e:
            return e.value

    @staticmethod
    def focus(func):
        def focus(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if type(result).__name__ == "generator":
                return self.active._handle_focus(None, result)
        return focus

class MetaElement(type):

    def __new__(cls, name, bases, attrs):
        attrs["Render"] = Render()
        return super().__new__(cls, name, bases, attrs)

class Element(metaclass=MetaElement):

    Render = Render()

    def __init__(self, pos: Vector):
        self.pos = pos

    def render(self):
        pass
