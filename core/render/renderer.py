from core.sys.single import Singleton
from core.sys import WIDTH, HEIGHT
from core.render.screen import Screen
import queue
import multiprocessing as mp
# try:
#     import multiprocessing as mp
# except ModuleNotFoundError:
#     import threading as mp
import PIL.ImageDraw

from core.hardware.display import Display

__all__ = ["Renderer"]

def clear_queue(q):
    data = []
    try:
        while True:
            data.append(q.get(False))
    except queue.Empty: pass
    return data

class Renderer(metaclass=Singleton):

    def __init__(self):
        self.draw = None
        self.image = None
        self._buffer = mp.JoinableQueue()
        self._changes = mp.JoinableQueue()
        self._frame_event = mp.Event()
        self._render_event = mp.Event()
        self._process_event = mp.Event()
        self._pause_event = mp.Event()

    def frame(self):
        self._buffer.put(self.image)
        self._frame_event.set()
        self._next()
        self._buffer.join()

    def _next(self):
        self.image = Screen().template().copy()
        self.draw = PIL.ImageDraw.Draw(self.image)

    def clear(self):
        self._next()

    def open(self):
        if not self._render_event.is_set():
            self._render_event.set()
            self._frame_event.clear()
            self._process_event.clear()
            self._pause_event.set()
            self._next()
            mp.Process(target=self._render_loop).start()
            mp.Process(target=self._render_cache).start()

    def close(self):
        self._render_event.clear()
        clear_queue(self._buffer)
        clear_queue(self._changes)
        self._frame_event.set()
        self._process_event.set()

    def pause(self):
        print("PAUSE")
        Screen().pause()
        self._pause_event.clear()

    def resume(self):
        print("RESUME")
        Screen().resume()
        self._pause_event.set()

    def _render_cache(self):
        cache = [[2 for y in range(HEIGHT)] for x in range(WIDTH)]
        while self._render_event.is_set():
            self._frame_event.wait()
            try:
                frame = (i for i in self._buffer.get(False).getdata())
                for y in range(HEIGHT):
                    for x in range(WIDTH):
                        pixel_value = next(frame)
                        if pixel_value != cache[x][y]:
                            self._changes.put((x, y, 1 if pixel_value == 0 else 0))
                        cache[x][y] = pixel_value
                self._changes.put(None)
                self._frame_event.clear()
                self._buffer.task_done()
                self._process_event.wait()
                self._process_event.clear()
            except queue.Empty:
                continue

    def _render_loop(self):
        while self._render_event.is_set():
            try:
                pixel = self._changes.get(False)
            except queue.Empty:
                continue
            if pixel is None:
                self._process_event.set()
                Display.show()
            else:
                Display.pixel(*pixel)
            self._changes.task_done()
