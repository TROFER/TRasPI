import core.log

log = core.log.name("Config")
PATH = "config/"
cfg = {}

def path(name="config/"):
    global PATH
    PATH = name

def load(filename="core", ext="cfg"):
    global cfg
    try:
        with open(PATH+filename+"."+ext, "r") as file:
            c = {"default":{}}
            sub = "default"

            for line in file:
                line = line.strip()
                if line == "": # getting rid of empty lines
                    continue
                elif line[0] == "[" and line[-1] == "]": # setting sub categories
                    sub = line[1:-1]
                    if sub not in c:
                        c[sub] = {}
                    continue

                #spliting into key and value
                line = line.split(" = ", 1)
                if len(line) == 1:
                    line.append("None")

                # type checking
                try:
                    if "." in line[1]:  line[1] = float(line[1]) # Float
                    else:   line[1] = int(line[1]) # Int
                except ValueError:
                    if line[1] == "None": line[1] = None # None
                    elif line[1].lower() in ("yes", "true", "no", "false"): # Bool
                        line[1] = (True if line[1].lower() in ("yes", "true") else False)
                    elif (line[1][0] == "[") and (line[1][-1] == "]" and ", " in line[1]): # Array
                        line[1] = line[1][1:-1].split(", ")

                c[sub][line[0]] = line[1]
    except IOError:
        log.err("Unable to Open File: {}.{}".format(filename, ext))
        return False
    cfg = c
    return cfg

def write(filename, data, ext="cfg"):
    try:
        with open(PATH+file_name+"."+ext, "w") as file:
            for sub in data:
                if type(data[sub]) == dict:
                    file.write("[{}]\n".format(sub))
                    for line in data[sub]:
                        file.write("{} = {}\n".format(line, "None" if data[sub][line] == None else data[sub][line]))
                    file.write("\n")
                else:
                    file.write("{} = {}\n".format(sub, "None" if data[sub] == None else data[sub]))
    except IOError:
        log.err("Unable to Open File: {}.{}".format(filename, ext), "Config")
        return False
    return True
