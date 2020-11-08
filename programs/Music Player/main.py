import core
from library import Library
from app import App
from window import browser, playlist, radio

############## TRASPI MUSIC PLAYER ###############
## Version: 1.1                                 ##
## Created By: Tristan Day                      ##
## Date: 2020                                   ##
##################################################

class Carousel(core.std.TabContainer):

    def __init__(self, library):
        super().__init__(
            browser.Main(library.db, "genre", title="Genres - Music Pl..."),
            browser.Main(library.db, "album", title="Albums - Music Pl..."),
            playlist.Main(library.db),
            radio.Browser(library.db))


class Main(core.render.Window):
    
    def __init__(self):
        self.splashscreen = core.render.element.Image(core.Vector(0, 0), App.asset.splashscreen, just_w='L')
        self._flag = False
        App.interval(self._await)
        super().__init__()

    def render(self):
        core.Interface.render(self.splashscreen)
        self._flag = True

    async def _await(self):
        if self._flag:
            self.library = Library()
            await Carousel(self.library)
            self.finish()


App.window = Main
main = App
