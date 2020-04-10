import multiprocessing as mp
import ctypes
import PIL.ImageDraw
import PIL.Image
from core.sys.constants import Constant
from core.driver.pipeline.display import Display

class Render:

    def __init__(self):
        self.__wgt_r = set() # Currently Rendered Widgets
        self.__wgt_s = set() # Submitted Widgets
        self._scene = False
        self.__update = True

        self.__template = PIL.Image.new("1", (Constant.width, Constant.height), 1)
        # self.__template
        self.__image = self.__template.copy()
        self.__draw = PIL.ImageDraw.Draw(self.__image)

        self.__renderer = Renderer()

    def submit(self, wgt):
        self.__wgt_s.add(wgt.render)

        if all(i==j for i,j in zip(wgt.copy(), wgt._widget)):
            wgt._widget = wgt.copy()
            wgt.volatile()
            self.__update = True

    def scene(self, flag: bool=None):
        self._scene = not self._scene if flag is None else flag

    def execute(self):
        if self.__update or self.__wgt_s != self.__wgt_r:
            self.__update = False
            self.__wgt_r = self.__wgt_s.copy()
            self.__wgt_s.clear()

            self.__image = self.__template.copy()
            self.__draw = PIL.ImageDraw.Draw(self.__image)

            for func in self.__wgt_r:
                func(self.__draw)

        self.__renderer.buffer_frame.put(self.__image)
        self.__renderer.event_frame.set()
        self.__renderer.buffer_frame.join()

    def open(self):
        self.__renderer.open()
    def close(self):
        self.__renderer.close()

class Renderer:

    def __init__(self):
        self.event_open = mp.Event()
        self.buffer_frame = mp.JoinableQueue()
        self.buffer_pixel = mp.JoinableQueue()

        self.event_frame = mp.Event()
        self.event_pixel = mp.Event()

        self.cache_frame = [[2 for y in range(Constant.height)] for x in range(Constant.width)]

    def open(self):
        if not self.event_open.is_set():
            self.event_open.set()
            self.event_frame.clear()
            self.event_pixel.clear()
            mp.Process(target=self.thread_frame).start()
            mp.Process(target=self.thread_pixel).start()

    def close(self):
        self.event_open.clear()
        self.event_frame.set()
        self.event_pixel.set()

    def thread_frame(self):
        while self.event_open.is_set():
            self.event_frame.wait()
            try:
                frame = self.buffer_frame.get(False)
                self.event_frame.clear()
                self.buffer_frame.task_done()
            except mp.queues.Empty: continue

            self.calculate_pixel(frame)

    def thread_pixel(self):
        while self.event_open.is_set():
            try:
                pixel = self.buffer_pixel.get(False)
            except mp.queues.Empty: continue

            if pixel is None:
                self.event_pixel.set()
                Display.show()
            else:
                Display.pixel(*pixel)
            self.buffer_pixel.task_done()

    def calculate_pixel(self, frame: PIL.Image.Image):
            data = iter(frame.getdata())

            for y in range(Constant.height):
                for x in range(Constant.width):
                    pixel = next(data)
                    if pixel != self.cache_frame[x][y]:
                        self.buffer_pixel.put((x, y, 1 if pixel == 0 else 0))
                        self.cache_frame[x][y] = pixel

            self.buffer_pixel.put(None)
            self.event_pixel.wait()
            self.event_pixel.clear()