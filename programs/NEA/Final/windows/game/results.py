import core
from core.render.element import Image
from app import App

class Main(core.render.Window):

    def __init__(self, game):
        # Elements

        self.title = Image()
        self.elements = []