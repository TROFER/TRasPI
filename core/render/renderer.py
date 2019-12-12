from core.render.single import Singleton
import core.render.template
import queue
# import multiprocessing as mp
import threading
import PIL
from gfxhat import lcd
# from core.dummy import lcd

__all__ = ["Render"]

WIDTH, HEIGHT = 128, 64

class Render(metaclass=Singleton):

    def __init__(self):
        self.draw = None
        self._image = None
        # self._buffer = mp.JoinableQueue()
        self._buffer = queue.Queue()
        # self._changes = mp.JoinableQueue()
        self._changes = queue.Queue()
        self._frame_event = threading.Event()
        self._render_event = threading.Event()

    def frame(self):
        self._buffer.put(self._image)
        self._frame_event.set()
        self._next()
        # print("START")
        self._buffer.join()
        # print("Hang")

    def _next(self):
        self._image = core.render.template.background.copy()
        self.draw = PIL.ImageDraw.Draw(self._image)

    def start(self):
        if not self._render_event.is_set():
            self._render_event.set()
            self._next()
            threading.Thread(target=self._render_loop).start()
            threading.Thread(target=self._render_cache).start()

    def close(self):
        self._render_event.clear()

    def _render_cache(self):
        cache = [[2 for y in range(HEIGHT)] for x in range(WIDTH)]
        while self._render_event.is_set():
            self._frame_event.wait()
            # print("Wait Frame")
            try:
                frame = (i for i in self._buffer.get(False).getdata())
                # print("FRAME", frame)
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        pixel_value = next(frame)
                        # print("PV", pixel_value)
                        if pixel_value != cache[x][y]:
                            # print("Diff Cache", pixel_value, x, y, loc)
                            self._changes.put((x, y, pixel_value))
                        cache[x][y] = pixel_value
                self._changes.put(None)
                # print("Put None in Changes")
                self._buffer.task_done()
                self._frame_event.clear()
            except queue.Empty:
                continue

    def _render_loop(self):
        while self._render_event.is_set():
            try:
                pixel = self._changes.get(False)
            except queue.Empty:
                continue
            if pixel is None:
                lcd.show()
            else:
                lcd.set_pixel(*pixel)
            self._changes.task_done()
