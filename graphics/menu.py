import core.log

#---Global Variables-----------------------------------------------------------#

log = core.log.name("menu")
LINE_BREAK = "-"*100 # — # -

#---Functions------------------------------------------------------------------#

def default_callback(action):
    action.parent.back()

#---Classes--------------------------------------------------------------------#

class Cursor:

    def __init__(self, max=0, start=0):
        self.pos = start
        self.max = max

    def move(self, spaces):
        self.pos += spaces
        while self.pos <= 0:
            self.pos += self.max
        while self.pos >= self.max:
            self.pos -= self.max

    def __call__(self):
        return self.pos

    def change(self, max=0, start=0):
        self.pos = start
        self.max = max

class Window:

    def __init__(self, callback=default_callback):
        self.pages = {}
        self.elements = {}
        self.path = []
        self.current = None
        self.cursor = Cursor()
        self.callback = callback
        self.buffer = ""

    def clean(self):
        self.pages = {}
        self.elements = {}
        self.items = []
        self.path = []
        self.current = None
        self.cursor = Cursor()
        self.buffer = ""

    def change(self):
        self.current = self.path[-1]
        self.current.on_load(self.current)
        self.cursor.change(len(self.current.actions))

    def back(self):
        if len(self.path) > 1:
            self.path.pop()
            self.change()
        else:
            print("QUIT") # TEMP

    def forward(self, page):
        self.path.append(page)
        self.change()

    def select(self):
        if isinstance(self.current, Page):
            self.current.actions[self.cursor()]()

    def move(self, spaces):
        self.cursor.move(spaces)

    def set_page(self, name):
        if str(name) in self.pages:
            self.forward(self.pages[str(name)])
        else:
            log.warn("Page: ", name, " can not be found")

    def element(self, name):
        if str(name) in self.elements:
            self.path.append(self.elements[str(name)])
            self.current = self.path[-1]
            self.current.on_load(self.current)
        else:
            log.warn(name, " is not of type 'Element'")

    def update(self):
        self.buffer = ""
        if isinstance(self.current, Page):
            if self.current.actions:
                self.buffer += self.current.draw()
                self.buffer += "\n"+LINE_BREAK+"\n"
                self.buffer += str(self.current.actions[self.cursor()].desc)
                self.buffer += "\n"+LINE_BREAK+"\n"
        elif isinstance(self.current, Element):
            self.buffer += self.current.draw()
            self.buffer += "\n"+LINE_BREAK+"\n"
        return self.buffer

class Page:

    def __init__(self, parent, name, *actions, load=None, draw=None):
        self.name = str(name)
        self.parent = parent
        self.actions = list(actions)
        self.parent.pages[self.name] = self
        self.on_load = load if load else self.on_load
        self.on_draw = draw if draw else self.on_draw

    def draw(self):
        self.on_draw(self)
        return "\n".join((("$ "+self.actions[i].draw() if i == self.parent.cursor() else "  "+self.actions[i].draw()) for i in range(len(self.actions))))

    def on_draw(self, *args, **kwargs):
        return True

    def on_load(self, *args, **kwargs):
        return True

class Action:

    def __init__(self, parent, func, type, msg, desc=None):
        self.parent = parent
        self.func = func
        self.type = type
        self.msg = msg
        self.desc = desc if desc else self.msg

    def __call__(self):
        if type(self.func).__name__ != "function":
            if self.type == "back":
                self.parent.back()
            elif self.type == "show":
                self.parent.set_page(self.func)
            elif self.type == "elmt":
                self.parent.element(self.func)
            else:
                self.parent.callback(self)
        else:
            self.func(self)

    def draw(self):
        return str(self.msg)

class Element:

    def __init__(self, parent, name, data="", load=None, draw=None):
        self.parent = parent
        self.name = str(name)
        self.parent.elements[self.name] = self
        self.data = data
        self.on_load = load if load else self.on_load
        self.on_draw = draw if draw else self.on_draw

    def __call__(self, *args):
        self.data = ""
        for i in args:
            self.data += str(i)

    def draw(self):
        self.on_draw(self)
        return str(self.data)

    def on_draw(self, *args, **kwargs):
        return True

    def on_load(self, *args, **kwargs):
        return True

#---Setup----------------------------------------------------------------------#

#---Main Loop------------------------------------------------------------------#

#---End------------------------------------------------------------------------#

"""
——————————
Location
——————————
Option 1
Option 2
Option 3
etc ...
——————————
Dialogue
Box
——————————
Misc Output
——————————
B1: Action, B2: Action, B3: Action
——————————
"""
