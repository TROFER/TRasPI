from gfxhat import backlight, lcd
try:
    lcd.clear()
    lcd.show()
    backlight.set_all(100,100,100)
    backlight.show()
    print("[OK] Backlight and LCD setup")
except:
    print("There was an error when clearing the screen")
