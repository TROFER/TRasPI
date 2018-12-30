import os
import core

def get_files(dir):
    try:
        os.listdir(dir)
    except IOError:
        return()


def menu():
    while dir != "!quit" or dir != "!Quit" #Upper and lower because of directory case sensitivity
    dir = input("""
    Simple File Manager for Pi
Please enter a directory to begin from\n>
    """)
    get_files(dir)


def main():
    menu()
