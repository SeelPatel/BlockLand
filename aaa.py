from pygame import *

display.set_mode((100,100))

count = 1
while 1:
    try:
        s = Surface((count,5000))
    except:
        print(count)
        break

    count += 100