#!/usr/bin/env python

import signal
import blk_lte_tstr.py
from gfxhat import touch

print("""touch.py
This shows how we can use scripts to link the buttons to certain actions
Press Ctrl+C to exit.
""")

def handler(channel, event):
    print("Button Pressed")
    blk_lte_tstr.main()

for x in range(6):
    touch.on(x, handler)

signal.pause()
