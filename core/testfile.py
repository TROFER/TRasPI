from gfxhat import touch
from time import sleep

def func1(ch, event):
    print("BUTTON 1")
    print("STARTING LOOP")
    for i in range(25):
        sleep(0.1)
    print("LOOP ENDED")

def func2(ch, event):
    print("Button 2")
    print("Im less angry than func1")

touch.on(1, func1)
touch.on(2, func2)

print("MAIN LOOP")
while True:
    pass 

print("PROGRAM END")
