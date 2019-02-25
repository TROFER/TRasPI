from gfxhat import touch, lcd, backlight, fonts

backlight.set_all(255,0, 225)
backlight.show()
lcd.clear()
for x in range(0,64):
    for y in range(0,128):
        lcd.set_pixel(y,x,1)
lcd.show()
