import json
from urllib.error import HTTPError, URLError
from urllib import request
import time
import datetime
from core.render.element import Text
from core.render.element import Rectangle
from core.vector import Vector
from core.interface import Interface
from core.sys.attributes import SysConstant
if SysConstant.platform == "POSIX":
    import gpiozero
    import psutil


class Panel:

    POSITIONS = [25, 35, 45, 55, 64]

    def __init__(self, title, fields, refresh=1):
        self.fields = fields
        self.speed = refresh
        self.elements = [Text(Vector(4, self.POSITIONS[i]), func(self), justify='L')
                         for i, func in enumerate(self.fields)]
        self.elements.append(Text(Vector(3, 15), title, justify='L'))
        self.elements.append(Rectangle(Vector(3, 12), Vector(64, 62)))

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        for i, element in enumerate(self.elements[:len(self.elements)-2]):
            element.text = self.fields[i]()


class WorldClock(Panel):

    LOCATIONS = ["London", "New%20York", "Tokyo", "Moscow"]

    def __init__(self):
        try:
            with open(f"{SysConstant.path}/core/panels.cache") as cache:
                self.cache = cache.read().splitlines()
        except FileNotFoundError:
            self.cache = [0, 0, 0, 0, 0, 0]
        if time.time() - int(self.cache[0]) > 46400:
            for i, location in enumerate(self.LOCATIONS, start=1):
                self.cache[i] = self._request(location)
            self.cache[0] = int(time.time())
            with open(f"{SysConstant.path}/core/panels.cache", 'w') as cache:
                cache.write("\n".join(map(str, self.cache)))
        super().__init__("World Clock", self.FIELDS, refresh=1)

    def _request(self, location):

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        with open(f"{SysConstant.path}user/openweatherkey.txt") as key:
            key = key.read()
        data = json.load(request.urlopen(f"{URL}q={location}&appid={key}"))
        return data["timezone"]

    def london(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[1]))))
        return f"Lond:{time.strftime('%H:%M')}"

    def newyork(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[2]))))
        return f"NYok:{time.strftime('%H:%M')}"

    def tokyo(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[3]))))
        return f"Toky:{time.strftime('%H:%M')}"

    def moscow(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[4]))))
        return f"Mosc:{time.strftime('%H:%M')}"

    def berlin(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[5]))))
        return f"berl:{time.strftime('%H:%M')}"

    FIELDS = [london, newyork,
              tokyo, moscow, berlin]


class HWinfo(Panel):

    def __init__(self):
        super().__init__("HW Info", self.FIELDS, refresh=1)

    def cpu_temp(self):
        return f"CPU°C: {round(gpiozero.CPUTemperature().temperature, 1)}°C"

    def cpu_usage(self):
        return f"CPU%: {psutil.cpu_percent()}%"

    def memory_usage(self):
        return f"Mem%: {psutil.virtual_memory().percent}%"

    def storage_free(self):
        return f"Strg%: {int(psutil.disk_usage('/').used) // int(psutil.disk_usage('/').total) * 100}%"

    FIELDS = [cpu_temp, cpu_usage,
              memory_usage, storage_free]


class Weather(Panel):

    LOCATION = "Isle%20of%20wight"

    def __init__(self):

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        with open(f"{SysConstant.path}user/openweatherkey.txt") as key:
            key = key.read()
        self.data = json.load(request.urlopen(
            f"{URL}q={self.LOCATION}&appid={key}"))
        super().__init__("Weather", self.FIELDS, refresh=1)

    def temperature(self):
        return f"Temp: {round(self.data['main']['temp'] - 273.1, 1)}°C"

    def pressure(self):
        return f"Pres: {self.data['main']['pressure']}Pa"

    def humidity(self):
        return f"Humi: {self.data['main']['humidity']}%"

    def wind_speed(self):
        return f"WSpd: {self.data['wind']['speed']}Mph"

    FIELDS = [temperature]


panels = [WorldClock(), HWinfo(), Weather()]
