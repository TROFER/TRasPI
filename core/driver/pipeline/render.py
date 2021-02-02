from ...error.attributes import SysConstant
import multiprocessing as mp
from .display import Display
if SysConstant.process:
    import PIL.ImageDraw
    import PIL.Image
    from ...asset.image import Template

    class Render:

        def __init__(self):
            self.__wgt_r = set() # Currently Rendered Widgets
            self.__wgt_s = set() # Submitted Widgets
            self._scene = False
            self.__update = True

            self.__template = PIL.Image.new("LA", (SysConstant.width, SysConstant.height), 1)
            self.__image = self.__template.copy()
            self.__draw = PIL.ImageDraw.Draw(self.__image)

            self.__renderer = Renderer()

        def template(self, template: Template):
            if not isinstance(template, Template):
                raise TypeError(f"Templates must be instance of '{Template.__name__}' and not '{template.__class__.__name__}'")
            self.__template = template.image

        def submit(self, wgt):
            self.__wgt_s.add(wgt.render)

            if not all(i==j for i,j in zip(wgt.copy(), wgt._widget)):
                wgt._widget = wgt.copy()
                wgt.volatile()
                self.__update = True

        def scene(self, flag: bool=None):
            self._scene = not self._scene if flag is None else flag

        def execute(self):
            if not self.__renderer.event_pause.is_set():
                return
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
            Display.initialize()
            self.__renderer.open()
        def close(self):
            self.__renderer.close()
            Display.terminate()

        def pause(self):
            self.__renderer.event_pause.clear()
        def resume(self):
            self.__renderer.event_pause.set()

class Renderer:

    def __init__(self):
        self.event_open = mp.Event()
        self.buffer_frame = mp.JoinableQueue()
        self.buffer_pixel = mp.JoinableQueue()

        self.event_pause = mp.Event()
        self.event_frame = mp.Event()
        self.event_image = mp.Event()
        self.event_pixel = mp.Event()

    def open(self):
        if not self.event_open.is_set():
            self.event_open.set()
            self.event_pause.set()
            self.event_frame.clear()
            self.event_image.clear()
            self.event_pixel.clear()
            mp.Process(target=self.thread_frame, name="FrameThread").start()
            mp.Process(target=self.thread_pixel, name="PixelThread").start()

    def close(self):
        self.event_open.clear()
        self.event_frame.set()
        self.event_image.set()
        self.event_pixel.set()

    def thread_frame(self):
        self.cache_frame = [[2 for y in range(SysConstant.height)] for x in range(SysConstant.width)]
        while self.event_open.is_set():
            self.event_pause.wait()
            self.event_frame.wait()
            try:
                frame = self.buffer_frame.get(False)
                self.event_frame.clear()
                self.buffer_frame.task_done()
            except mp.queues.Empty: continue

            self.calculate_pixel(frame)

    def thread_pixel(self):
        while self.event_open.is_set():
            self.event_pause.wait()
            self.event_pixel.wait()
            try:
                pixel = self.buffer_pixel.get(False)
            except mp.queues.Empty: continue

            if pixel is None:
                self.event_image.set()
                self.event_pixel.clear()
                Display.show()
            else:
                Display.pixel(*pixel)
            self.buffer_pixel.task_done()

    def calculate_pixel(self, frame: 'PIL.Image.Image'):
            data = iter(frame.getdata())

            self.event_pixel.set()
            for y in range(SysConstant.height):
                for x in range(SysConstant.width):
                    pixel = next(data)
                    if pixel != self.cache_frame[x][y]:
                        self.buffer_pixel.put((x, y, 1 if pixel == 0 else 0))
                        self.cache_frame[x][y] = pixel

            self.buffer_pixel.put(None)
            self.event_image.wait()
            self.event_image.clear()
