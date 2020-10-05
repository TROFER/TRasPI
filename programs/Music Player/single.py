import core
from core.std import menu
from index import Index
from core import Vector

class Main(menu.Menu):

    def __init__(self):
        self.library = Index.scan()
        
        elements = []
        for genre in self.library:
            elements.append(menu.MenuElement(
                *[Text(Vector(0, 0), genre.name, justify='L'), Text(Vector(128, 0), len(genre.albums), justify='R')],
                data = genre
                select = 

                )
