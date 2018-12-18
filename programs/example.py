import core.log
import core.config

log = core.log.name("Example")

def main():
    core.config.load("thiswillnotworkhahaha")
    print("Hello World")
    for i in range(2):
        print(i)
    print("Goodbye World")
    log.info("The example is now ending")
    raise ValueError("dwadwa")
