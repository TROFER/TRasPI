from core.render.single import Singleton
import core.render.template
import queue
import multiprocessing as mp
import PIL
from gfxhat import lcd

__all__ = ["Render"]

WIDTH, HEIGHT = 128, 64

class Render(metaclass=Singleton):

    def __init__(self):
        self.draw = None
        self._image = None
        self._buffer = mp.JoinableQueue()
        self._changes = mp.JoinableQueue()
        self._frame_event = mp.Event()
        self._render_event = mp.Event()

    def frame(self):
        self._buffer.put(self._image)
        self._frame_event.set()
        self._next()
        self._buffer.join()

    def _next(self):
        self._image = core.render.template.background.copy()
        self.draw = PIL.ImageDraw.Draw(self._image)

    def start(self):
        if not self._render_event.is_set():
            self._next()
            mp.Process(target=self._render_loop).start()
            mp.Process(target=self._render_cache).start()
            self._render_event.set()

    def close(self):
        self._render_event.clear()

    def _render_cache(self):
        cache = [2 for x in range(WIDTH) for y in range(HEIGHT)]
        while self._render_event.is_set():
            self._frame_event.wait()
            try:
                frame = (i for i in self._buffer.get(False).getdata())
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        pixel_value = next(frame)
                        loc = x * WIDTH + y
                        if pixel_value != cache[loc]:
                            self._changes.put((x, y, pixel_value))
                        cache[loc] = pixel_value
                        self._changes.put(None)
                self._buffer.task_done()
            except queue.Empty:
                continue

    def _render_loop(self):
        while self._render_event.is_set():
            self._frame_event.wait()
            pixel = 1
            while pixel is not None:
                try:
                    pixel = self._changes.get(False)
                    lcd.set_pixel(*pixel)
                    self._changes.task_done()
                except queue.Empty:
                    break
            lcd.show()
            self._frame_event.clear()
