from PIL import ImageFont


def font_size(height, path=None, text="sample text"):
    height = int(height)
    if path is None:
            path="D:/Documents/Programing/TrasPi Operating System/fonts/font.ttf"
    def printout(size, height, path):
        print(f"{'#'*75}\nFont Size: {size} Path: {path[0:25]}... is closest match for {height}px\n{'#'*75}")
    results, maxsize = [], 100
    try:
        for size in range(1, maxsize, 1):
            x, y = (ImageFont.truetype(path, size).getsize(text))
            if y > height:
                results.append((y - height, size))
            elif height > y:
                results.append((height - y, size))
            else:
                printout(size, height, path)
        printout((min(results)[1]), height, path)
        
    except KeyboardInterrupt:
        quit()


def pixels(size, path=None, text=None):
    try:
        if path is None:
            path="D:/Documents/Programing/TrasPi Operating System/fonts/font.ttf"
        if text is None:
            text = "Sample Text"
        x, y = (ImageFont.truetype(path, int(size)).getsize(text))
        print(f"{'#'*75}\nUsing Font {path[0:30]}... 'Sample Text', Font Size: {size}:\nWidth: {x} Pixels\nHeight: {y} Pixels\n{'#'*75}\n")
    except KeyboardInterrupt:
        quit()
    except ImportError:
        wait = input("PIL Failed to Import")


def helpmenu():
    print("""
Commands:\n1. pixels - Takes args size, path, text. Returns font XY in pixels
2. font size - Takes Takes args size, path, text. Returns a font size closest matching to desired height""")


def main():
    while True:
        commands = {"pixels": pixels, "font size": font_size, "help": helpmenu}
        str_command = input("Type Help for Instructions\n> ").lower().split(" -")
        try: 
            command = commands[str_command[0]]
            command(*str_command[1:len(str_command)])
        except KeyError:
            print(f"{str_command[0]} is not a command")
        

main()
