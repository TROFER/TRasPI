import json
from urllib.error import HTTPError, URLError
from urllib import request
import datetime
from core.render.element import Text
from core.vector import Vector
from core.interface import Interface
import gpiozero
import psutil

# ADD PATHS


class Panel:

    POSITIONS = [15, 25, 35, 45, 55]

    def __init__(self, title, fields, refresh=1):
        self.fields = fields
        self.speed = refresh
        self.elements = [Text(Vector(4, POSITIONS[i]), func(), justify='L')
                         for i, func in enumerate(self.fields)]
        self.elements.append(Text(Vector(4, 5), title, justify='L'))

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        for i, element in enumerate(self.elements[:len(self.elements)-1]):
            element.text = self.fields[i]()


class WorldClock(Panel):

    def __init__(self):

        LOCATIONS = ["London", "New%20York", "Tokyo", "Moscow", "Berlin"]
        FIELDS = [self.london, self.newyork,
                  self.tokyo, self.moscow, self.berlin]

        with open(f"{core.sys.PATH}") as cache:
            self.cache = cache.read().splitlines()
        if time.time() - int(self.cache[0]) > 46400:
            for i, location in enumerate(LOCATIONS, start=1):
                self.cache[i] = self._request(location)
            self.cache[0] = time.time()
            with open(f"{core.sys.PATH}", 'w') as cache:
                cache.write("\n".join(self.cache))
        super().__init__("World Clock", FIELDS, refresh=1)

    def _request(self, location):

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        with open(f"{core.sys.PATH}user/openweatherkey.txt") as key:
            key = key.read()
        data = json.load(request.urlopen(f"{URL}q={location}&appid={key}"))
        return data["timezone"]

    def london(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=self.cache[1])))
        return f"Lond:{time.strftime('%H:%M')}"

    def newyork(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=self.cache[2])))
        return f"NYok:{time.strftime('%H:%M')}"

    def tokyo(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=self.cache[3])))
        return f"Toky:{time.strftime('%H:%M')}"

    def moscow(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=self.cache[4])))
        return f"Mosc:{time.strftime('%H:%M')}"

    def berlin(self):
        time = datetime.datetime.now(datetime.timezone(
            datetime.timedelta(seconds=self.cache[5])))
        return f"berl:{time.strftime('%H:%M')}"


class HWinfo(Panel):

    FIELDS = [self.cpu_temp, self.cpu_usage,
              self.memory_usage, self.storage_free]

    def __init__(self):
        super().__init__("HW Info", FIELDS, refresh=1)

    def cpu_temp(self):
        return f"CPU°C: {round(gpiozero.CPUTemperature().temperature, 1)}°C"

    def cpu_usage(self):
        return f"CPU%: {psutil.cpu_percent()}%"

    def memory_usage(self):
        return f"Mem%: {psutil.virtual_memory().percent}%"

    def storage_free(self):
        return f"Strg%: {int(psutil.disk_usage('/').used) // int(psutil.disk_usage('/').total) * 100}%"


class Weather(Panel):

    LOCATION = "Isle%20of%20wight"
    FIELDS = [self.temperature]

    def __init__(self):

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        with open(f"{core.sys.PATH}user/openweatherkey.txt") as key:
            key = key.read()
        self.data = json.load(request.urlopen(
            f"{URL}q={location}&appid={key}"))
        super().__init__("Weather", FIELDS, refresh=1)

    def temperature(self):
        return f"Temp: {round(self.data['main']['temp'] - 273.1, 1)}°C"

    def pressure(self):
        return f"Pres: {self.data['main']['pressure']}Pa"

    def humidity(self):
        return f"Humi: {self.data['main']['humidity']}%"

    def wind_speed(self):
        return f"WSpd: {self.data['wind']['speed']}Mph"


panels = [WorldClock(), HWinfo(), Weather()]
