# noinspection PyUnresolvedReferences
from gfxhat import lcd, backlight, touch
from PIL import Image, ImageFont, ImageDraw
import multiprocessing as mp
import queue
import time
import textwrap

# Default Globals For Menu
WIDTH, HEIGHT = 128, 64
TEMPLATE = Image.open("/home/traspi/core/menu.template").convert("P")


def handle_press(func):
    def handle_press(self, ch, event):
        if event == "press":
            return func(self, ch, event)

    return handle_press


def handle_release(func):
    def handle_release(self, ch, event):
        if event == "release":
            return func(self, ch, event)

    return handle_release


def handle_hold(func):
    def handle_hold(self, ch, event):
        if event == "hold":
            return func(self, ch, event)
    return handle_hold


# -------------------------Multiprocessing and Render---------------------------#
'''
class Render:
    _draw = None
    _image = None
    _buffer = mp.JoinableQueue()
    _frame_event = mp.Event()
    _render_event = mp.Event()

    def __new__(cls):
        return cls

    @classmethod
    def draw(cls) -> ImageDraw.ImageDraw:
        return cls._draw

    @classmethod
    def frame(cls):
        cls._buffer.put(cls._image)
        cls._frame_event.set()
        cls._next()
        cls._buffer.join()

    @classmethod
    def _next(cls):
        cls._image = TEMPLATE.copy()
        cls._draw = ImageDraw.Draw(cls._image)

    @classmethod
    def start(cls):
        if not cls._render_event.is_set():
            cls._next()
            mp.Process(target=cls._render_loop).start()
            cls._render_event.set()

    @classmethod
    def close(cls):
        cls._render_event.clear()

    # @staticmethod
    # def _image_processing(cls, arg):
    #     image, x, y = arg
    #     return image.getpixel((x, y))

    @classmethod
    def _render_loop(cls):
        # times = []
        # with mp.Pool() as pool:# Number of Stripes
        # cache = [2 for x in range(WIDTH) for y in range(HEIGHT)]
        while cls._render_event.is_set():
            cls._frame_event.wait()
            try:
                image = cls._buffer.get()
                # print("RENDER")
                # time_s = time.time()

                # it = pool.imap(cls._image_processing, ((image, x, y) for x in range(WIDTH) for y in range(HEIGHT)),
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
                cls._buffer.task_done()
            except queue.Empty:
                break
            cls._frame_event.clear()
'''


class Render:
    _frames = mp.JoinableQueue()
    _changes = mp.JoinableQueue()
    _event = mp.Event()
    _draw = None

    @classmethod
    def get_changes(cls):
        cache = [[2 for y in range(64)] for x in range(128)]
        while not cls._event.is_set():
            frame = list(cls._frames.get().getdata())
            for x in range(128):
                for y in range(64):
                    pixel_value = next(frame)
                    if pixel_value != cache[x][y]:
                        cls._changes.put((x, y, pixel_value))
                    cache[x][y] = pixel_value

    @classmethod
    def set_changes(cls):
        while not cls._event.is_set():
            try:
                while cls._changes is not queue.Empty:
                    change = cls._changes.get()
                    lcd.setpixel(change[0], change[1], change[2])
                lcd.show()
            except queue.Empty:
                pass

    @classmethod
    def start_render(cls):
        if __name__ == '__main__':
            p_get_changes = mp.Process(target=cls.get_changes, args=(cls,))
            p_set_changes = mp.Process(target=cls.set_changes, args=(cls,))
            p_get_changes.start(), p_set_changes.start()
            p_get_changes.join(), p_set_changes.join()



class Screen:
    _screen = None

    def __new__(cls, *args, **kwargs):
        if cls._screen is None:
            cls._screen = super().__new__(cls)
            return cls._screen

    def __init__(self):
        self.showing = None
        self.children = set()
        self.pos = (0, 0)

    @classmethod
    def screen(cls):
        return cls._screen

    @classmethod
    def render(cls):
        if cls._screen.showing is not None:
            cls._screen.showing.render()

    @classmethod
    def focus(cls, element=None):
        if element is not None:
            cls._screen.showing = element


class Element:

    def __init_subclass__(cls):
        for i in range(1, 7):
            fname = "handle_" + str(i)
            sf = getattr(super(cls, cls), fname)
            cf = getattr(cls, fname)
            if cf != sf:
                def wrap_handler(func):
                    def handle(self, ch, event):
                        handle = func(self, ch, event)
                        if type(handle).__name__ == "generator":
                            self._handle_finish(None, handle)

                    return handle

                setattr(cls, fname, wrap_handler(cf))

    def __init__(self, parent, pos=(0, 0)):
        self.parent = parent
        self.parent.children.add(self)
        self.children = set()
        self.pos = pos
        self.vars = {
        }

    def __repr__(self) -> str:
        return "<{}: {}>".format(self.__class__.__name__, self.parent)

    def __hash__(self):
        return self.__repr__().__hash__()

    def render(self):
        pass

    def handle_1(self, ch, event):
        pass

    def handle_2(self, ch, event):
        pass

    def handle_3(self, ch, event):
        pass

    def handle_4(self, ch, event):
        pass

    def handle_5(self, ch, event):
        pass

    def handle_6(self, ch, event):
        pass

    def focus(self, generator=None):
        for i, f in enumerate(
                (self.handle_1, self.handle_2, self.handle_3, self.handle_4, self.handle_5, self.handle_6)):
            touch.on(i, f)
        Screen.focus(self)
        self._generator = generator

    def finish(self, value=None):
        self.parent.focus()
        if self.generator is not None:
            self.parent._handle_finish(value, self.generator)
        return value

    def _handle_finish(self, value, generator):
        try:
            element = generator.send(value)
            if isinstance(element, Element):
                element.focus(handle)
        except StopIteration:
            pass


class TextContainer(Element):

    def __init__(self, parent, pos, text="Default Text", font="/home/traspi/fonts/font.ttf", size=10, colour=1,
                 justify="C", char_limit=None):
        self._text = text
        self.size = size
        self._justify = justify
        self.colour = colour
        super().__init__(parent, pos)
        self.font = ImageFont.truetype(font, self.size)
        self.char_limit = char_limit
        self.compute()

    def __repr__(self) -> str:
        return "TEXT {} {} {}".format(self.text, self.justify, self.size)

    def compute(self):
        self.font_size = self.font.getsize(self.text)
        self._calc_justify()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self.compute()

    @property
    def justify(self) -> str:
        return self._justify

    @justify.setter
    def justify(self, value: str):
        self._justify = value
        self.compute()

    def _calc_justify(self):
        if self.justify == "C":
            self.position = (self.pos[0] - (self.font_size[0] // 2), self.pos[1] - (self.font_size[1] // 2))
        elif self.justify == "L":
            self.position = (self.pos[0], self.pos[1] - (self.font_size[1] // 2))
        elif self.justify == "R":
            self.position = (self.pos[0] - self.font_size[0], self.pos[1] - (self.font_size[1] // 2))
        else:
            # Centre justify if no justification matches
            self.justify = "C"
            self.position = (self.pos[0] - (self.font_size[0] // 2), self.pos[1] - (self.font_size[1] // 2))

    def render(self):
        Render.draw().text(self.position, self.text[0:self.char_limit] if self.char_limit is None else self.text,
                           self.colour, self.font)


class Square(Element):

    def __init__(self, parent, pos):
        super().__init__(parent, pos)


# -----------------------Core Graphics Functions Classes------------------------#

class Menu(Element):

    def __init__(self, parent, pos, *labels):
        super().__init__(parent, pos)
        self.labels = [TextContainer(self, (3, 32), text, justify="L", colour=0) for text in labels]
        self.up_arrow = TextContainer(self, (WIDTH // 2, 16), text="/\\")
        self.down_arrow = TextContainer(self, (WIDTH // 2, 48), text="\\/")
        self.selected_index = 0

    @handle_press
    def handle_1(self, ch, event):
        print("UP ARROW")
        if self.selected_index < len(self.labels) - 1:
            print(self.selected_index)
            self.selected_index += 1

    @handle_press
    def handle_2(self, ch, event):
        print("DOWN ARROW")
        if self.selected_index > 0:
            print(self.selected_index)
            self.selected_index -= 1

    @handle_press
    def handle_5(self, ch, event):
        print("ENTER BUTTON")
        print("Get IntegerInput Value")
        val = yield IntegerInput(self, 0, 0, 0)
        print("GOT THE D:", val)
        # self.finish(self.labels[self.selected_index])

    def render(self):
        self.labels[self.selected_index].render()
        if self.selected_index != 0:
            self.up_arrow.render()
        if self.selected_index != len(self.labels):
            self.down_arrow.render()


'''
class IntegerInput(Element):

    def __init__(self, parent, number, units_index, min, max=None):
        super().__init__(parent, pos)
        self.units = [1, 10, 50, 100, 500, 1000, 5000]
        number, units_index
        self.unit_left = TextContainer(parent, (0.2, 0.5))
        self.min, self.max = min, max
        self.unit_right = TextContainer(parent, (0.8, 0.5))
        self.number = TextContainer(parent, (0.8, 0.5))

    @handle_press
    def handle_1(self, ch, event):
        if self.units_index < len(self.units):
            self.units_index += 1

    @handle_press
    def handle_2(self, ch, event):
        if self.units_index != 0:
            self.units_index -= 1

    @handle_press
    def handle_3(self, ch, event):
        self.finish()

    @handle_press
    def handle_4(self, ch, event):
        if self.number - self.units[self.units_index] > self.min:
            self.number -= self.units[self.units_index]

    @handle_press
    def handle_5(self, ch, event):
        self.finish(self.number)

    @handle_press
    def handle_6(self, ch, event):
        if self.number + self.units[self.units_index] < self.max:
            self.number += self.units[self.units_index]

    def render(self):
        self.unit_left.render()
        self.unit_right.render()
        self.number.render()
'''


# -----------------------Callable Graphics Functions----------------------------#


'''def interger_input(max, min=0):
    get_input = IntegerInput()
'''


def start():
    execute = True
    Render.start()
    try:
        while execute:
            Screen.render()
            Render.frame()
    finally:
        Render.close()


Screen()

Menu(Screen.screen(), (0, 0), "Five", "Six", "Seven", "Eight").focus()

start()


# --------------------------------Hardware Control------------------------------#

def touch_config(func, config=None, doleds=False):
    if config is None:
        config = [0, 1, 2, 3, 4, 5]
    for button in config:
        touch.on(button, func)
        if doleds:
            touch.set_led(button, 1)


def touch_led(leds=None, value=0):
    if leds is None:
        leds = [0, 1, 2, 3, 4, 5]
    for led in leds:
        touch.set_led(led, value)


def backlight_fill(colours=(225, 225, 225), percent=70):
    _colours = [colour / 100 for colour in colours]
    backlight.set_all(round(_colours[0] * percent), round(_colours[1] * percent), round(_colours[2] * percent))
    backlight.show()


def backlight_gradient(colours):
    for led in range(5):
        _colours = [int(hex_colour, 16) for hex_colour in [colours[led][i:i + 2] for i in range(0, 6, 2)]]
        backlight.set_pixel(led, _colours[0], _colours[1], _colours[2])
    backlight.show()


def clear_screen():
    lcd.clear(), lcd.show()
# -----------------------------End Hardware Control-----------------------------#
