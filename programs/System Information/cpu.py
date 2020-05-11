import os
import subprocess

import core
from home.app import App
from core import Vector
from core.render.element import Line, Rectangle, Text

try:
    import psutil
    import gpiozero
except ImportError:
    print("Warning: Some dependancies could not be found")


class Graph:

    BUFFER_SIZE = 10

    def __init__(self):
        self.buffer = [0 for i in range(self.BUFFER_SIZE)]

    def plot(self, data):
        self.buffer.append(data)
        del self.buffer[-1]
    
    def trend(self):
        if self.buffer[0] > self.buffer[-1]:
            return True
        elif self.buffer[0] < self.buffer[-1]:
            return False
        else:
            None


class Main(core.render.Window, Graph):

    def __init__(self):
        self.elements = [
            Text(Vector(3, 5), "CPU - System Information", justify='L'),
            Text(Vector(3, 15), ""),
            Text(Vector(3, 20), ""),
            Text(Vector(3, 25), ""),
            Text(Vector(3, 30), "CPU Load"),
            Rectangle(Vector(3, 35), Vector(126, 37)),
            Line(Vector(0, 36), Vector(128, 36), width=2),
            Text(Vector(3, 40), "CPU Speed"),
            Rectangle(Vector(3, 45), Vector(126, 47)),
            Line(Vector(0, 46), Vector(128, 46), width=2)]
        App.interval(self.refresh)
    
    
    def refresh(self):
        self.elements[1].text = f"CPU Load: {psutil.cpu_percent()}%"
        self.elements[2].text = f"CPU Temp: {round(gpiozero.CPUTemperature().temperature, 1)}°C {"/\\" if self.cput_graph else "\\/"}"
        os.system("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
        self.elements[6].pos2 = Vector(int(psutil.cpu_percent()), 37)
        self.elements[4].text = f"CPU Speed: {subprocess.check_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq", shell=True).decode()
        self.elements[9].pos2 = Vector(int(subprocess.check_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq", shell=True).decode()), 37)

        
class Handle(core.input.event.Handle):

    window = Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(0)
        
        