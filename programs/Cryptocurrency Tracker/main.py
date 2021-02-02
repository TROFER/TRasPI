import core
import urllib.request
import json
import time
from datetime import datetime
from core.render.element import Text, Line, Image
from app import App
from core import Vector
from core.hw import Backlight

class Main(core.render.Window):

    URL = "https://api.cryptonator.com/api/ticker/"
    CURRENCIES = [
        ["Ethereum", [248, 36, 41], 'eth-usd', App.asset.ethereum],
        ["Bitcoin", [34, 88, 96], 'btc-usd', App.asset.bitcoin],
        ["Litecoin", [199, 12, 100], 'ltc-usd', App.asset.bitcoin],
        ["Dogecoin", [54, 97, 100], 'doge-usd', App.asset.bitcoin]]

    def __init__(self):
        self.index = 0
        self.elements = [
            Text(Vector(3, 5), f"{self.CURRENCIES[self.index][0]}", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "Market Rate:", font=App.asset.title_font, justify='L'),
            Text(Vector(3, 26), "", font=App.asset.title_font, justify='L'),
            Text(Vector(3, 37), "", justify='L'),
            Line(Vector(3, 42), Vector(80, 42), width=2),
            Text(Vector(3, 50), "Change: (Past Hr)", justify='L'),
            Image(Vector(115, 13),self.CURRENCIES[self.index][3])]
        App.interval(self.refresh, 60)
    
    async def show(self):
        self.refresh()
        Backlight.fill(self.CURRENCIES[self.index][1])
    
    def render(self):
        for element in self.elements:
            core.interface.render(element)
    
    def refresh(self):
        data = self.request()
        if data is not None:
            self.elements[3].text = f"{round(float(data['ticker']['price']), 4)} USD"
            self.elements[4].text = f"At: {datetime.utcfromtimestamp(data['timestamp']).strftime('%H:%M')}"
            self.elements[6].text = f"{data['ticker']['change'][:6]} (Past Hr)"
    
    def switch(self):
        self.refresh()
        Backlight.fill(*self.CURRENCIES[self.index][1])
        self.elements[0].text = f"{self.CURRENCIES[self.index][0]}"
        self.elements[7].image = self.CURRENCIES[self.index][3]
        
    def request(self):
        try:
            _req = urllib.request.Request(f"{self.URL}{self.CURRENCIES[self.index][2]}", headers={'User-Agent': 'Mozilla/5.0'})
            return json.load(urllib.request.urlopen(_req))
        except:
            return None

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            if window.index < len(window.CURRENCIES) -1:
                window.index += 1
                window.switch()

        async def left(null, window: Main):
            if window.index != 0:
                window.index -= 1
                window.switch()

App.window = Main
main = App       
