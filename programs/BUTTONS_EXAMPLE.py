#!/usr/bin/env python

import signal
from time import sleep
import blk_lte_tstr
from gfxhat import touch, lcd, backlight, fonts

print("""touch.py
This shows how we can use scripts to link the buttons to certain actions
Press Ctrl+C to exit.
""")

lcd.clear()

def handler(channel, event):
    print("Button Pressed")
    if channel == 0:
        r = 255
        g,b = 0,0
    elif channel == 1:
        g = 255
        r,b = 0,0
    elif channel == 2:
        b = 255
        r,g = 0,0
    sleep(1)
    blk_lte_tstr.main_script(r,g,b)

for x in range(6):
    touch.on(x, handler)

signal.pause()
