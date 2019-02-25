from gfxhat import lcd
from random import randint

lcd.clear()
lcd.show()
for i in range(0,100):
    lcd.set_pixel((randint(0,127)),(randint(0,63)),1)
    lcd.show()
