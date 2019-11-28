from render.enums import Button, Event
from render.handle import Handler
from render.screen import Screen

__all__ = ["Window"]

class Window:

    _handles = [lambda *arg: None] * 6

    def __init__(self):
        self.elements = {}

    def render(self):
        pass

    def show(self):
        Screen().show(self)

class Handle(Handler):

    key = Button.UP
    window = Window

    def press(self):
        print("PRESS EVENT ON BUTTON UP IN", self.window)
