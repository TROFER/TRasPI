from core.render.single import Singleton
import core.render.template
import queue
import multiprocessing as mp
import PIL
from gfxhat import lcd
import trace
# from core.dummy import lcd

__all__ = ["Render"]

WIDTH, HEIGHT = 128, 64

def tracer(func):
    def tracer(*args, **kwargs):
        t = trace.Trace(ignoremods=(mp, queue, PIL, gfxhat), ignoredirs=("/usr/local/lib/",))
        t.runfunc(func, *args, **kwargs)
        t.results().write_results()
    return tracer

class Render(metaclass=Singleton):

    def __init__(self):
        self.draw = None
        self._image = None
        self._buffer = mp.JoinableQueue()
        self._changes = mp.JoinableQueue()
        self._frame_event = mp.Event()
        self._render_event = mp.Event()
        self._process_event = mp.Event()
        self._current_frame = -1

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
            self._render_event.set()
            self._next()
            mp.Process(target=self._render_loop).start()
            mp.Process(target=self._render_cache).start()

    def close(self):
        self._render_event.clear()

    @tracer
    def _render_cache(self):
        cache = [[2 for y in range(HEIGHT)] for x in range(WIDTH)]
        # count = 0
        while self._render_event.is_set():
            try:
                self._frame_event.wait()
                try:
                    frame = (i for i in self._buffer.get(False).getdata())
                    # count += 1
                    for y in range(HEIGHT):
                        for x in range(WIDTH):
                            pixel_value = next(frame)
                            if pixel_value != cache[x][y]:
                                self._changes.put((x, y, pixel_value))
                            cache[x][y] = pixel_value
                    self._changes.put(None)
                    self._buffer.task_done()
                    self._frame_event.clear()
                    self._process_event.wait()
                    self._process_event.clear()
                except queue.Empty:
                    continue
            except BaseException:
                pass

    @tracer
    def _render_loop(self):
        while self._render_event.is_set():
            try:
                try:
                    pixel = self._changes.get(False)
                except queue.Empty:
                    continue
                if pixel is None:
                    # self._current_frame = pixel
                    lcd.show()
                    self._process_event.set()
                else:
                    lcd.set_pixel(*pixel)
                self._changes.task_done()
            except BaseException:
                pass
