import core.log

#---Global Variables-----------------------------------------------------------#

log = core.log.name("menu")
LINE_BREAK = "-"*100 # —

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
        self.path = []
        self.current = None
        self.cursor = Cursor()
        self.callback = callback

    def clean(self):
        self.pages = {}
        self.elements = []
        self.path = []
        self.current = None
        self.cursor = Cursor()

    def back(self):
        if len(self.path) > 1:
            self.path.pop()
            self.current = self.path[-1]
            self.cursor.change(len(self.current))
        else:
            print("QUIT")

    def forward(self, page):
        self.path.append(page)
        self.current = self.path[-1]
        self.cursor.change(len(self.current))

    def select(self):
        if isinstance(self.current, Page):
            self.forward(self.current[self.cursor()])
        elif isinstance(self.current, Element):
            self.current[self.cursor()]()
        print(self.current)

    def move(self, spaces):
        self.cursor.move(spaces)

    def set_page(self, name):
        self.forward(self.pages[name])

class Page:

    def __init__(self, parent, name, *elements):
        self.name = str(name)
        self.parent = parent
        self.elements = list(elements)
        self.parent.pages[self.name] = self

    def __len__(self):
        return self.elements.__len__()

    def __getitem__(self, key):
        return self.elements[key]

    def draw(self):
        return "\n".join((("$ "+self.elements[i].name if i == self.parent.cursor() else "  "+self.elements[i].name) for i in range(len(self.elements))))

class Element:

    def __init__(self, name, desc, *actions):
        self.name = name
        self.actions = list(actions)
        self.desc = desc

    def __call__(self):
        self.action()

    def __len__(self):
        return self.actions.__len__()

    def __getitem__(self, key):
        return self.actions[key]

    def draw(self):
        return "\n".join((("$ "+self.actions[i].draw() if i == self.actions[i].parent.cursor() else "  "+self.actions[i].draw()) for i in range(len(self.actions))))

class Action:

    def __init__(self, parent, string, type, msg):
        self.parent = parent
        self.string = string
        self.type = type
        self.msg = str(msg)

    def __call__(self):
        print(self.type, self.string)
        self.parent.callback(self)

    def draw(self):
        return self.msg

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
