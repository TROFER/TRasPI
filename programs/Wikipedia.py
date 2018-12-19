import wikipedia
import core.log
log = core.log.name("Wikipedia")
#Ver pre-finish

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
    lang, ans_len, command = ("en"), 2, ("") #Defult settings

    while command != "quit()":
        try:
            command = input("Enter a Query or Command: > ").lower()
            if command == "length()":
                ans_len =edit_len(ans_len)
            elif command == "quit()":
                quit()
            else:
                wikipedia.set_lang(lang)
                print(wikipedia.summary(command, sentences=ans_len))
        except:
            log.warn("Somthing went wrong, Please try again")
