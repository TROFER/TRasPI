from random import randint
from time import sleep
print("Welcome to the number guessing game!\n")
def scores():
    try:
        f=open("scoresheet.txt",'r')
        text = f.read().splitlines()
        text.sort()
        print("\nThe current high scores are...\n{}\n{}\n{}\n{}\n{}".format(text[0],text[1],text[2]))
    except IndexError:
        print("There where not enough scores to display")
    except IOError:
        print("File missing or deleted...\nCreating new file...\n")
        f=open("scoresheet.txt",'w')
        f.close()

def main_game(dev):
    code, guess, guesses, count, name = [], [], 1, 0, input("Enter a Nickname: ")
    for i in range(0,4):
        code.append(randint(0,9))
    if dev == True:
        print(code)
    while guess !=code:
        count, guess = 0, []
        try:
            for i in range(0,4):
                diget = (input("Enter a code: "))
                for i in range(0,4):
                    guess.append(diget[i])
            if guess !=code:
                for i in range(0,4):
                        if guess[i] == code[i]:
                            count = count +1
                print(count,"of the numbers where correct")
                guesses+=1
                sleep(0.5)
        except ValueError:
            print("Numbers Only")
        except KeyboardInterrupt:
            quit()
    print("Congratulations you won!\nYou took",guesses,"to win!")
    try:
        f=open("scoresheet.txt",'a')
        f.write ("\n{} {}".format(guesses,name))
        f.close()
    except IOError:
           print("Highscores file missing or deleted\nRun scores command to create a new file\n")
def menu():
    while True:
        try:
            command = input("> ").lower()
            if command == "play":
                dev = False
                main_game(dev)
            elif command == "scores":
                scores()
            elif command == "quit":
                quit()
            elif command == "dev":
                dev = True
                main_game(dev)
            elif command == "help":
                print("Type play to start the game\ntype scores to veiw high scores\ntype quit to exit the game")
            else:
                print("Not a valid option")
        except KeyboardInterrupt:
            print("\nType quit to quit")

def main():
    menu()

main()
