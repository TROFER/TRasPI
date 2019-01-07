import os
#import core

def display(files,Curent_Dir):
    files.sort()
    temp = file.len()
    print("Files in:",Curent_Dir,"\n")
    for i in range(temp):
        print(files[i])


def fetch_files(Prev_Dir, Curent_Dir, input_cmd):
    files = os.listdir(input_cmd)
    Prev_Dir.append(input_cmd)
    Curent_Dir = input_cmd
    return(Prev_Dir, Curent_Dir, input_cmd, files)


def input_dir(No_back, Prev_Dir, Curent_Dir, files):
    input_cmd = input("Enter a comand: ") #""
    if input_cmd == "!quit" or input_cmd == "!Quit": #Input is case sensitive
        quit()
    elif input_cmd == "!back" or input_cmd == "!Back":
        prev(No_back, Prev_Dir, Curent_Dir, input_cmd)
    try:
        temp = os.listdir(input_cmd)
        fetch_files(Prev_Dir, Curent_Dir, input_cmd, files)
        display(files, Curent_Dir)
    except IOError:
        #Tom sould I re-call function or loop
        print("Directory not found ")


def main():
    No_back = 0
    Prev_Dir = []
    Curent_Dir = ""
    files = []
    print("""
       Simple File Explorer
       type !quit for Quit
!back to return to previous directory
    """) #Add "go up directory option"
    input_dir(No_back, Prev_Dir, Curent_Dir, files)



main()
