import os
#import core

def input_dir(No_back, Prev_Dir, Curent_Dir):
    input_cmd = input("Enter a comand: ") #""
    if input_cmd == "!quit" or input_cmd == "!Quit": #Input is case sensitive
        quit()
    elif input_cmd == "!back" or input_cmd == "!Back":
        prev(No_back, Prev_Dir, Curent_Dir)
    try:
        temp = os.listdir(input_cmd)
        fetch_files(No_back, Prev_Dir, Curent_Dir)
    except IOError:
        #Tom sould I re-call function
        print("Directory not found ")


def main():
    No_back = 0
    Prev_Dir = []
    Curent_Dir = ""
    print("""
       Simple File Explorer
       type !quit for Quit
!back to return to previous directory
    """) #Add "go up directory option"
    input_dir(No_back, Prev_Dir, Curent_Dir)



main()
