import os
import sys

argc, argv = len(sys.argv), sys.argv

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def sys(command):
    os.system(command)
