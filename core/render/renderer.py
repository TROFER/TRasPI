from core.render.single import Singleton
import core.render.template
import queue
import multiprocessing as mp
import PIL
from gfxhat import lcd

__all__ = ["Render"]

class Render(metaclass=Singleton):

    def __init__(self):
        self._frames = mp.JoinableQueue()
        self._changes = mp.JoinableQueue()
        self._event = mp.Event()
        self.draw = None

    def get_changes(self):
        cache = [[2 for y in range(64)] for x in range(128)]
        while not self._event.is_set():
            try:
                frame = list(self._frames.get(False).getdata())
                for x in range(128):
                    for y in range(64):
                        pixel_value = frame[y * 64 + x]
                        if pixel_value != cache[x][y]:
                            self._changes.put((x, y, pixel_value))
                        cache[x][y] = pixel_value
                self._changes.put(None)
                self._frames.task_done()
            except queue.Empty:
                continue

    def set_changes(self):
        while not self._event.is_set():
            try:
                while self._changes is not queue.Empty:
                    change = self._changes.get(False)
                    if change is not None:
                        lcd.set_pixel(change[0], change[1], change[2])
                    else:
                        lcd.show()
                    self._changes.task_done()
            except queue.Empty:
                pass

    def start_render(self):
        self._next()
        p_get_changes = mp.Process(target=self.get_changes)
        p_set_changes = mp.Process(target=self.set_changes)
        p_get_changes.start(), p_set_changes.start()
            # p_get_changes.join(), p_set_changes.join()

    def stop_render(self):
        self._event.set()

    def frame(self):
        self._frames.put(self._image)
        self._next()
        self._frames.join()

    def _next(self):
        self._image = core.render.template.background.copy()
        self.draw = PIL.ImageDraw.Draw(self._image)
