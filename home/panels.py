import datetime
import json
import time
from urllib import request
from urllib.error import HTTPError, URLError

from core.asset.font import Font
from core.interface import Interface
from core.render.element import Rectangle, Text
from core.sys.attributes import SysConstant
from core.vector import Vector

if SysConstant.platform == "POSIX":
    import gpiozero
    import psutil


class Panel:

    POSITIONS = [25, 35, 45, 55, 64]
    FONT = Font(f"bitocra7", 7)

    def __init__(self, title, fields, refresh=1):
        self.fields = fields
        self.speed = refresh
        self.elements = [Text(Vector(2, self.POSITIONS[i]), func(self), font=self.FONT, justify='L')
                         for i, func in enumerate(self.fields)]
        self.elements.append(
            Text(Vector(2, 17), title, font=self.FONT, justify='L'))
        self.elements.append(Rectangle(Vector(0, 12), Vector(50, 62)))

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        for i, element in enumerate(self.elements[:len(self.elements)-2]):
            element.text = self.fields[i](self)


class WorldClock(Panel):

    LOCATIONS = ["London", "New%20York", "Berlin", "Moscow"]

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
        return f"Londo:{time.strftime('%H:%M')}"

    def newyork(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[2]))))
        return f"NYork:{time.strftime('%H:%M')}"

    def moscow(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[3]))))
        return f"Mosco:{time.strftime('%H:%M')}"

    def berlin(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=int(self.cache[4]))))
        return f"Berli:{time.strftime('%H:%M')}"

    FIELDS = [london, newyork,
              moscow, berlin]


class HWinfo(Panel):

    def __init__(self):
        super().__init__("HW Info", self.FIELDS, refresh=1)

    def cpu_temp(self):
        return f"CPUC: {round(gpiozero.CPUTemperature().temperature, 1)}C"

    def cpu_usage(self):
        return f"CPU%: {psutil.cpu_percent()}%"

    def memory_usage(self):
        return f"Mem%: {psutil.virtual_memory().percent}%"

    def storage_free(self):
        return f"Strg%: {psutil.disk_usage('/').percent}%"

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
        return f"Temp: {round(self.data['main']['temp'] - 273.1, 1)}C"

    def pressure(self):
        return f"Pres: {self.data['main']['pressure']}Pa"

    def humidity(self):
        return f"Humi: {self.data['main']['humidity']}%"

    def wind_speed(self):
        return f"WSpd: {round(self.data['wind']['speed'], 1)}Mph"

    FIELDS = [temperature, pressure, humidity, wind_speed]


panels = [Weather(), HWinfo(), WorldClock()]
