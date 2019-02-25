from gfxhat import touch
from os import system
#import programs index

def index(sel):
    if sel == 1:
        #the code shoud call the first function acording to the index
        programs()
    elif sel == 2:
        settings()
    elif sel == 3:
        os.system("sudo halt")

def verify(sel,menu_range):
    if  selection > menu_range or selection < 1:
        return False
    else:
        return True

def handler(channel):
    if channel = 0:
        sel+=1
        #add some screen interactions here like selection indication etc
    elif channel = 1:
        sel+=1
        #see above anotataion
    elif channel = 4:
        menu_range = 3
        if verify(sel, menu_range) == True:
            index(sel)
        else:
            return

while True:
    touch.on(x, handler)

signal.pause()
