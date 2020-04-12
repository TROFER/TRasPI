from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.render.element import TextBox
from core.render.element import Rectangle
from core.vector import Vector
from core.sys.attributes import SysConfig
import time
import panels

class Main(Window):

    # template = core.asset.Template("std::window", path="window.template")

    def __init__(self):
        self.index = 0
        self.elements = [
            Text(Vector(3, 5), f"{SysConfig.system_name}", justify='L'), 
            Text(Vector(126, 5), time.strftime("%I:%M%p"), justify='R'),
            Text(Vector(0, 0), ">", justify='R'),
            TextBox(Vector(127, 18), "Run Program", justify='R'),
            TextBox(Vector(127, 30), "System Settings", justify='R'),
            TextBox(Vector(127, 42), "Power Options", justify='R')]
        self.panels = []

    def render(self):
        for element in self.elements:
            Interface.render(element)
    
    def refresh(self):
        pass
        
