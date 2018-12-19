import wikipedia
import core.log
log = core.log.name("Wikipedia")

def main():
    print("Basic Wikipedia Query\nComands:\nlength() for setting result length (Sentences)")
    lang = ("en")
        while True:
            try:
                command = input("> ").lower()
                if command == "length()":
                    while ans_len > 0 and ans_len < 15:
                        try:
                            while True:
                                ans_len = int(input("Enter New Result Length: "))
                        except ValueError:
                            log.warn("Please enter an integer (1-15)")





'''
    question = ("Coca-Cola")
wikipedia.set_lang("en")
print(wikipedia.summary(question, sentences=2))
'''
