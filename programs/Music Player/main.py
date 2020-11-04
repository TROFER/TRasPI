import core
from library import Library
from app import App
from window import browser

############## TRASPI MUSIC PLAYER ###############
## Version: 1.1                                 ##
## Created By: Tristan Day                      ##
## Date: 2020                                   ##
##################################################

class Main(core.std.TabContainer):

    def __init__(self):
        self.library = Library()
        super().__init__(
            browser.Top(self.library.db, "genre", title="Genres - Music Pl..."),
            browser.Top(self.library.db, "album", title="Albums - Music Pl..."))

App.window = Main
main = App
