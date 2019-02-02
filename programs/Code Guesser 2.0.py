import random
dificulty, custom, code, code_colour, gueses = 0,0,[],"",0

def win(nickname,gueses,dificulty):
    print("Congratulations you won in",gueses,"moves")
    try:
        file = open("scores.txt",'a')
        file.write("\n{} {} {}".format(gueses,nickname,dificulty))
        file.close()
    except IOError:
        print("Highscores file missing or deleted\nRun scores to create a new one\n")


def colour_mode(code):
    nickname = input("Enter a nickname: ")
    if code[0] == 0 or code[0] == 4:
        code_colour = "red"
    elif code[0]== 1 or code[0] == 5:
        code_colour = "yellow"
    elif code[0] == 2 or code[0] == 6:
        code_colour = "green"
    elif code[0] == 3 or code[0] == 7:
        code_colour = "blue"
    gueses = 1
    while True:
            answer = input("Enter a colour: ").lower().strip().replace(" ", "")
            if answer == code_colour:
                win(nickname,gueses,dificulty)
                break
            else:
                print("That was not the correct colour please try again")
                gueses = gueses+1




def main():
    print("Main Menu\nType Help For Help")
    comand = input("> ").lower().strip().replace(" ", "")
    if comand == "play":
        selection = input("Please chose a dificulty:\n\n\tEasy: Four Colours Guess the right one\n\tMedium: Classic 4 Diget Number\n\tHard: Guess a Five Diget Number\n\tCustom: Enter a custom number of digets to crack the code\n\n> ").lower().strip().replace(" ", "")
        if selection == "easy":
            dificulty = 0
            main_game()
        elif selection == "medium":
            dificulty = 1
            main_game()
        elif selection == "hard":
            dificulty = 2
            main_game()
        elif selection == "custom":
            dificulty = 3
            custom = int(input("Please enter a custom dificulty: "))
            main_game()

def generate_code(dificulty,code,custom):
    if dificulty == 0:
        max_value, runs = 7, 1
    elif dificulty == 1:
        max_value, runs = 9, 4
    elif dificulty == 2:
        max_value, runs = 9, 5
    elif dificulty == 3:
        max_value, runs = 9, custom
        print("Runs is",runs)
    for i in range(0,runs):
        print("Adding A Peice of Code")
        print(max_value)
        number = random.randint(0,max_value)
        code.append(number)
        print(code)
    return(code)


def main_game():
    generate_code(dificulty,code,custom)
    if dificulty == 0:
        colour_mode(code)
    else:
        number_mode()


main()
