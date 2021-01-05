from time import strftime

import core
from core import Vector
from core.render.element import Text, Image, Line, Marquee

from app import App
from request import CurrentData
from submenu import Options as OptionsMenu


class Main(core.render.Window):

    LOCATION = App.const.default_location
    WEATHER_KEY = {"01": 1, "02": 9, "03": 2, "04": 2,
                   "09": 3, "10": 4, "11": 7, "13": 5, "50": 2}
    MARQUEE_SPEED = 1
    INDEX = 0

    def __init__(self):
        self.elements = {
            "qstatus": Text(Vector(1, 30), "0",
                            font=App.asset.DSEG_Weather,  justify='L'),
            "clock0": Text(Vector(115, 11), strftime("%-I:%M"),
                          font=App.asset.DSEG7ClassicMini_Regular,  justify='R'),
            "clock1": Text(Vector(128, 18), strftime("%p"), justify='R'),
            "status": Text(Vector(128, 25), "Loading...", 
                           font=App.asset.Bitocra7, justify='R'),
            "temp": Text(Vector(129, 33), "",  justify='R'),
            "div": Line(Vector(65, 38), Vector(126, 38)),
            "data0": Text(Vector(128, 43), "",  font=App.asset.Bitocra7, justify='R'),
            "data1": Text(Vector(128, 50), "",  font=App.asset.Bitocra7, justify='R'),
            "data2": Text(Vector(128, 57), "",  font=App.asset.Bitocra7, justify='R')}
        self.request()
        self.tabs = [
            [self.current.feelsLike, self.current.temperatureMax,
                self.current.temperatureMin],
            [self.current.temperatureEnv, self.null, self.null],
            [self.current.pressure, self.current.humidity, self.current.visibility],
            [self.current.windSpeed, self.current.windDeg, self.current.windGust],
            [self.current.sunrise, self.current.sunset, self.null]]
        App.interval(self.refresh)
        App.interval(self.request, App.var.refresh_period * 60)
        App.interval(self.cycle, 10)
        super().__init__()

    def render(self):
        for element in self.elements.values():
            core.interface.render(element)

    def request(self):
        self.current = CurrentData(self.LOCATION)

    def refresh(self):
        e = self.elements
        e["qstatus"].text = str(
            self.WEATHER_KEY[self.current.icon()[:-1]])
        e["clock0"].text = strftime("%-I:%M")
        e["clock1"].text = strftime("%p")
        e["status"].text = self.current.description()
        e["temp"].text = self.current.temperature()
        for i in range(0, 3):
            e[f"data{i}"].text = self.tabs[self.INDEX][i]()
        self.elements = e

    def cycle(self):
        if self.INDEX == len(self.tabs) - 1:
            self.INDEX = 0
        else:
            self.INDEX += 1

    def null(self):
        return ""


class Handler(core.input.Handler):

    window = Main

    class press:

        async def up(self, window):
            await OptionsMenu(window)

        async def down(self, window):
            window.finish()


App.window = Main
main = App
