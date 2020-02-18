import board
import displayio
import busio
from math import cos
from math import sin
from math import asin
from math import radians
from time import time
from time import sleep
from random import randint

display = board.DISPLAY
splash = displayio.Group(max_size=50)

# Background
BGbitmap = displayio.Bitmap(display.width, display.height, 1)
BGpalette = displayio.Palette(1)
BGpalette[0] = 0x50b0a8
BGsprite = displayio.TileGrid(BGbitmap, x=0, y=0, pixel_shader=BGpalette)
splash.append(BGsprite)

# Palette for gauge bitmap
palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0x97f3e8 #lightturq
palette[2] = 0x50b0a8 #medturk
palette[3] - 0x408890 #darkturq
palette.make_transparent(0)

# Create gauge bitmap
gaugeBmp = displayio.Bitmap(display.width, display.height, len(palette))
gauge = displayio.TileGrid(gaugeBmp, pixel_shader=palette)
splash.append(gauge)

# show splash group
display.show(splash)

r = 70 #outer gauge radius
iRad = 20 #inner gauge radius

def gaugeDraw(newVal, oldVal, r, iRad, gaugeCenterX, gaugeCenterY, color, setUp = False):
    y = gaugeCenterY
    if newVal == oldVal:
        pass
    elif newVal > oldVal:
        totalDegrees = newVal - oldVal
        print(totalDegrees)
        sleep(1)
        for i in range(180, totalDegrees):
            print("BIGGER I: " + str(i))
            y = y+1
            x1 = int(cos(radians(i)) * r) + gaugeCenterX#outter x
            print("x1: " + str(x1))
            x2 = int(cos(asin(radians(y/iRad)))*iRad) + gaugeCenterX
            #print("x2: " + str(x2))
            vLineRange = x2 - x1
            #print("range " + str(vLineRange))
            sleep(1)
            for q in range(vLineRange):
                x = x1 + q
                gaugeBmp[x,y] = color
    elif newVal < oldVal:
        maxY = int(sin(radians(oldVal)) * r) + gaugeCenterY
        minY = int(sin(radians(newVal)) * r) + gaugeCenterY
        totalDegrees = oldVal - newVal
        print(totalDegrees)
        for i in range(maxY, minY, -1):
            print("I: " + str(i))
            y = y-1
            x1 = int(cos(radians(i)) * r) + gaugeCenterX
            print("x1: " + str(x1))
            a2 = int(asin(radians(y/iRad)))
            a2 = a2 - i
            x2 = int(cos(asin(radians(y/iRad)))*iRad) + gaugeCenterX
            print("x2: " + str(x2))
            vLineRange = abs(x1 - x2)
            print("Vertical Line Lenght: " +str(vLineRange))
            for q in range(vLineRange):
                x = x1 + q
                gaugeBmp[x,y] = 3
 
firstRowX = 95
firstRowY = 95

rando2 = randint(179, 315)
rando3 = randint(180, 315)
rando4 = randint(189, 315)

for i in range(3):
    x = (firstRowX + (r*2*i))
    gaugeDraw(180, 315, r+4, iRad+4, x, firstRowY, 3)

while True:
    rando1 = randint(179, 315)
    for i in range(3):
        x = (firstRowX + (r*2*i))
        gaugeDraw(rando1, rando2, r, iRad, x, firstRowY, 1)
        rando2 = rando1
    sleep(1)
