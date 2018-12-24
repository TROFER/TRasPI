#$PIP: wikipedia,
import wikipedia
import core.log
log = core.log.name("Wikipedia")
#Ver prefinish v2

def edit_len(ans_len):
    while True:
        try:
            ans_len = int(input("Enter New Result Length: "))
            break
        except ValueError:
            log.warn("Please enter an integer (1-15)")
    return (ans_len)

def main():
    print("Basic Wikipedia Query\nComands:\nlength() for setting result length (Sentences)\nquit() for quitting the application\n") #Menu
    lang, ans_len, command, cmd_char = ("en"), 2, (""), "!" #Defult settings

    while True:
        try:
            command = input("Enter a Query or Command: > ").lower()
            print(command)
            if command[:len(cmd_char)] == cmd_char:
                command = command[len(cmd_char):]
                if command == "length":
                    ans_len = edit_len(ans_len)
                elif command == "quit":
                    quit()
            else:
                wikipedia.set_lang(lang)
                print(wikipedia.summary(command, sentences=ans_len), "\n")
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            log.warn("Page not found, please try again")
