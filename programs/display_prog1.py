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
#################################TEXT########################
cursorposy = 20
for cursorposx in range(0,64,4):
    for letter in range(0,7):
        for p in range(0,3):
                lcd.set_pixel(cursorposx,(cursorposy+a),1)

lcd.show()
