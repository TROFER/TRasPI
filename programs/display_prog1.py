from gfxhat import lcd
lcd.clear()
lcd.show()
for header in range(0,128):
    lcd.set_pixel(header,0,1)
for line in range(20,63,20):
    for bar in range(0,128):
        lcd.set_pixel(bar,line,1)
for footer in range(0,128):
    lcd.set_pixel(header,63,1)
lcd.show()
