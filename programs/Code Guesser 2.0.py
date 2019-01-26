from random import randint

dificulty =0
custom = 9
code = []


def main():
    print("Main Menu\nType Help For Help")
    comand = input("> ").lower().strip().replace(" ", "")
    if comand == "play":
        selection = input("Please chose a dificulty:\nEasy: Four Colours Guess the right one\nMedium: Classic 4 Diget Number\nHard: Guess a Five Diget Number\nCustom: Enter a custom number of digets to crack").lower().strip().replace(" ", "")
        if selection == "easy":





def generate_code(dificulty,code,custom):
    if dificulty == 0:
        max, runs = 4, 1
    elif dificulty == 1:
        max, runs = 9, 4
    elif dificulty == 2:
        max, runs = 9, 5
    elif dificulty == 3:
        max, runs = 9, custom
    for i in range(0,runs):
        code.append(randint(0,max))
    print(code)
    return(code)




def main_game():
    generate_code(dificulty,code,custom)

main()
