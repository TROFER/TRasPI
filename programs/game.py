import core.log
import grpahics.gui
from random import randint
from time import sleep

log = core.log.name("game")

def play_game():
    graphics.gui.cls()






def menu():
    print("""
##################
   1.Play Game
##################
  2.Achevements
    3.Credits
     5.Quit
    """)
    while True:
        try:
            menu_opt = int(input("Please select an option: "))
            if menu_opt > 0 and menu_opt < 6:
                if menu_opt == 1:
                    play_game()
                elif menu_opt == 2:
                    achevements()
                elif menu_opt == 3:
                    credits()
                elif menu_opt == 5:
                    quit()
                else:
                    pass
        except ValueError:
            log.warn("Enter a valid option")

def main():
    #Add progress loader
    menu()
