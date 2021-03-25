import time

import core
from app import App
from core import Vector
from core.render.element import Line, Text
from request import pool, ticker


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(1, 5), "Nano...", justify="L"),
            Text(Vector(
                127, 5), f'{core.hw.Battery.percentage()}% {time.strftime("%H:%M")}', justify="R"),
            Line(Vector(0, 10), Vector(128, 10)),
            Text(Vector(1, 16), "Balance:", justify="L"),
            Text(Vector(1, 24), "Balance GBP:", justify="L"),
            Text(Vector(1, 32), "Current Hashrate:", justify="L"),
            Text(Vector(1, 40), "Workers:", justify="L"),
            Text(Vector(1, 48), "Average Hashrate (1hr):", justify="L"),
            Line(Vector(2, 53), Vector(126, 53)),
            Text(Vector(1, 59), "1p", justify="L"),
            Text(Vector(127, 59), "16p", justify="R"),
            Line(Vector(15, 59), Vector(115, 59), width=2)]
        App.interval(self.refresh, 15)
        App.interval(self.status)
        self.refresh()

    def status(self):
        self.elements[1].text = f'{core.hw.Battery.percentage()}% {time.strftime("%H:%M")}'

    def refresh(self):
        e = self.elements
        e[3].text = f"Balance: {pool.balance()} M"
        e[4].text = f"Balance GDP: {round(float(ticker.request('xmr-gbp')['ticker']['price']) * float(pool.balance()), 5)}"
        e[5].text = f"Current: {pool.current_hashrate()} h/s"
        e[6].text = f"Workers: {pool.worker_count()}"
        e[7].text = f"Average (1hr): {pool.average_hashrate()} h/s"
        e[11].pos2 = Vector(
            constrain(float(ticker.request("xmr-gbp")["ticker"]["price"]) * float(pool.balance()), 0, 16, 15, 115), 59)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def down(null, window: Main):
            window.finish()


def constrain(n, start1, stop1, start2, stop2):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)
