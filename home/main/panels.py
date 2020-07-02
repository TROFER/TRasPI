import core
from app import App

import time
import datetime
import json
import urllib.request
try:
    import psutil
    import gpiozero
except ImportError:
    pass

import traceback

TIME_FORMAT = "%H:%M"

class Panel:

    POSITIONS = [26, 36, 46, 56, 65]

    def __init__(self, title: str, *fields: callable):
        self.fields_funcs = fields
        self.fields = [core.element.Text(core.Vector(2, self.POSITIONS[i]), "TxT", App.asset.panel_font, justify="L") for i in range(len(self.fields_funcs))]
        self.elements = {
            core.element.Text(core.Vector(2, 17), title, App.asset.panel_font, justify="L"),
            core.element.Rectangle(core.Vector(0, 13), core.Vector(50, 62)),
        }

        self.refresh()

    def render(self):
        for element in (*self.elements, *self.fields):
            core.Interface.render(element)

    def refresh(self):
        for func, elm in zip(self.fields_funcs, self.fields):
            try:
                elm.text = func()
            except Exception as err:
                elm.text = " ~ERR"

class WorldClock(Panel):

    URL = "http://api.openweathermap.org/data/2.5/weather?"
    LOCATIONS = [("Londn", "London"), ("NYork", "New%20York"), ("Berln", "Berlin"), ("Mscow", "Moscow")]

    def __init__(self):
        self.reload_cache()
        super().__init__("Clock", *self.get_funcs())

    def reload_cache(self):
        curr = int(time.time())
        if curr - App.var.time_cache[0] > 46400:
            App.var.time_cache[0] = curr
            for index, data in enumerate(self.LOCATIONS, start=1):
                App.var.time_cache[index] = self.request(data[1])

    def get_funcs(self):
        funcs = []
        for index, data in enumerate(self.LOCATIONS, start=1):
            def store_vars(index, name):
                def func():
                    time = datetime.datetime.now(datetime.timezone(
                        datetime.timedelta(seconds=int(App.var.time_cache[index]))))
                    return f"{name}:{time.strftime(TIME_FORMAT)}"
                return func
            funcs.append(store_vars(index, data[0]))
        return funcs

    def request(self, location):
        try:
            with open(f"{core.sys.const.path}user/openweatherkey.txt") as key:
                key = key.read()
            data = json.load(urllib.request.urlopen(f"{self.URL}q={location}&appid={key}"))
            return data["timezone"]
        except Exception as e:
            return None

    def refresh(self):
        self.reload_cache()
        super().refresh()

class HWInfo(Panel):

    def __init__(self):
        self.funcs = [self.cpu_temp, self.cpu_usage, self.memory_usage, self.storage_free]
        super().__init__("HW Info", *self.funcs)

    def cpu_temp(self):
        return f"CPUC: {round(gpiozero.CPUTemperature().temperature, 1)}C"

    def cpu_usage(self):
        return f"CPU%: {psutil.cpu_percent()}%"

    def memory_usage(self):
        return f"Mem%: {psutil.virtual_memory().percent}%"

    def storage_free(self):
        return f"Strg%: {psutil.disk_usage('/').percent}%"

class Weather(Panel):

    LOCATION = "Isle%20of%20wight"
    URL = "http://api.openweathermap.org/data/2.5/weather?"

    def __init__(self):
        self.reload_cache()
        self.funcs = [self.temperature, self.pressure, self.humidity, self.wind_speed]
        super().__init__("Weather", *self.funcs)

    def temperature(self):
        return f"Temp: {round(self.data['main']['temp'] - 273.1, 1)}C"

    def pressure(self):
        return f"Pres: {self.data['main']['pressure']}Pa"

    def humidity(self):
        return f"Humi: {self.data['main']['humidity']}%"

    def wind_speed(self):
        return f"WSpd: {round(self.data['wind']['speed'], 1)}Mph"

    def reload_cache(self):
        curr = int(time.time())
        if curr - App.var.weather_cache[0] > 46400:
            App.var.weather_cache[0] = curr
            App.var.weather_cache[1] = self.request(self.LOCATION)
        self.data = App.var.weather_cache[1]

    def request(self, location: str):
        try:
            with open(f"{core.sys.const.path}user/openweatherkey.txt") as key:
                key = key.read()
            return json.load(urllib.request.urlopen(f"{self.URL}q={location}&appid={key}"))
        except Exception as e:
            return {}