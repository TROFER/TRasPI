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
            self._render_event.set()

    def close(self):
        self._render_event.clear()

    # @staticmethod
    # def _image_processing(self, arg):
    #     image, x, y = arg
    #     return image.getpixel((x, y))

    def _render_loop(self):
        # times = []
        # with mp.Pool() as pool:# Number of Stripes
        # cache = [2 for x in range(WIDTH) for y in range(HEIGHT)]
        while self._render_event.is_set():
            self._frame_event.wait()
            try:
                image = self._buffer.get()
                # print("RENDER")
                # time_s = time.time()

                # it = pool.imap(self._image_processing, ((image, x, y) for x in range(WIDTH) for y in range(HEIGHT)),
                # chunksize=16)
                for x in range(WIDTH):
                    for y in range(HEIGHT):
                        lcd.set_pixel(x, y, image.getpixel((x, y)))

                lcd.show()

                # time_e = time.time()
                # time_t = time_e - time_s
                # times.append(time_t)
                # print(len(times), sum(times) / len(times))
                # cache = image
                self._buffer.task_done()
            except queue.Empty:
                break
            self._frame_event.clear()

# class Render(metaclass=Singleton):
#
#     def __init__(self):
#         self._frames = mp.JoinableQueue()
#         self._changes = mp.JoinableQueue()
#         self._event = mp.Event()
#         self.draw = None
#
#     def get_changes(self):
#         cache = [[2 for y in range(64)] for x in range(128)]
#         while not self._event.is_set():
#             try:
#                 frame = list(self._frames.get(False).getdata())
#                 for x in range(128):
#                     for y in range(64):
#                         pixel_value = next(frame)
#                         if pixel_value != cache[x][y]:
#                             self._changes.put((x, y, pixel_value))
#                         cache[x][y] = pixel_value
#                 self._changes.put(None)
#             except queue.Empty:
#                 continue
#
#     def set_changes(self):
#         while not self._event.is_set():
#             try:
#                 while self._changes is not queue.Empty:
#                     change = self._changes.get(False)
#                     if change is not None:
#                         lcd.setpixel(change[0], change[1], change[2])
#                     else:
#                         lcd.show()
#             except queue.Empty:
#                 pass
#
#     def start_render(self):
#         if __name__ == '__main__':
#             self._next()
#             p_get_changes = mp.Process(target=self.get_changes)
#             p_set_changes = mp.Process(target=self.set_changes)
#             p_get_changes.start(), p_set_changes.start()
#             # p_get_changes.join(), p_set_changes.join()
#
#     def stop_render(self):
#         self._event.set()
#
#     def frame(self):
#         self._frames.put(self._image)
#         self._frame_event.set()
#         self._next()
#         self._frames.join()
#
#     def _next(self):
#         self._image = core.render.template.background.copy()
#         self.draw = PIL.ImageDraw.Draw(self._image)
