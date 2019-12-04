from core.vector import Vector
from core.render.enums import Button, Event
from core.render.handle import Handler
from core.render.screen import Screen
from core.render.renderer import Render

__all__ = ["Window", "Element"]

class MetaWindow(type):

    def __new__(cls, name, bases, attrs):
        attrs["_handles"] = [None] * 6
        return super().__new__(cls, name, bases, attrs)

class Window(metaclass=MetaWindow):

    _handles = [None] * 6

    def __init__(self):
        self.elements = {}

    def render(self):
        pass

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
        except StopIteration:
            pass

    @staticmethod
    def focus(func):
        def focus(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if type(result).__name__ == "generator":
                self.active._handle_focus(None, result)
        return focus

class Element:

    Render = Render()

    def __init__(self, pos: Vector):
        self.pos = pos

    def render(self):
        pass
