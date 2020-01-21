import core.error
from core.vector import Vector
from core.render.enums import Button, Event
from core.render.handle import Handler
from core.render.screen import Screen
from core.render.renderer import Renderer
from core.asset import Template


__all__ = ["Window", "Element"]

class MetaWindow(type):

    def __new__(cls, name, bases, attrs):
        if "template" in attrs:
            template = attrs["template"]
            if isinstance(template, str):
                attrs["template"] = Template(template)
        return super().__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        cls._handles = [i for i in cls._handles]
        return super().__init__(name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        self = super().__call__(*args, **kwargs)
        # self.elements = {}
        return self

class Window(metaclass=MetaWindow):

    _handles = [None] * 6
    template = "std"

    def __init__(self):
        self.elements = {}

    def render(self):
        pass

    def show(self):
        Screen().show(self)
        Renderer().clear()

    def finish(self, value=None):
        parent, generator = Screen().call_lost()
        parent.show()
        if generator is not None:
            parent._handle_focus(value, generator)
        Renderer().resume()
        return value

    def _handle_focus(self, value, generator):
        try:
            window = generator.send(value)
            if isinstance(window, Window):
                Screen().call_focus(generator, self)
                window.show()
        except StopIteration as e:
            return e.value
        except GeneratorExit as e:
            print("FOCUS WINDOW", e)
            raise core.error.FocusError(window) from e

    @staticmethod
    def focus(func):
        def focus(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if type(result).__name__ == "generator":
                return Screen().active._handle_focus(None, result)
        return focus

Screen().show(Window())

class MetaElement(type):

    def __new__(cls, name, bases, attrs):
        attrs["Render"] = Renderer()
        return super().__new__(cls, name, bases, attrs)

class Element(metaclass=MetaElement):

    Render = Renderer()

    def __init__(self, pos: Vector):
        self._pos = pos
        self._pos_abs = self._pos

    def render(self):
        pass

    @property
    def pos_abs(self):
        return self._pos_abs

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: Vector):
        self._pos = value
        self._pos_abs = self._offset(value)

    def _offset(self, value: Vector):
        return value
