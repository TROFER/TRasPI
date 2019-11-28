from PIL import Image
import time
frame = Image.open("/home/traspi/programs/weather/concept.png").convert('P')
start = time.time()
data = (frame.getdata())
data = list(data)
print(time.time()-start)
for value in range(len(data)):
    if data[value] == 1:
        data[value] = "@"
    else:
        data[value] = ""
with open("dump.txt", 'w') as outputfile:
    outputfile.write(str(data))
