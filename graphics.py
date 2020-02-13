import board
import displayio
import busio
from math import cos
from math import sin
from math import radians
from time import time
from time import sleep
from random import randint
display = board.DISPLAY
splash = displayio.Group(max_size=100)

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

def translate(val, OldMin, OldMax, NewMin = 180, NewMax = 90):
    OldRange = (OldMax - OldMin)
    NewRange = (NewMax - NewMin)
    newVal = (((val - OldMin) * NewRange) / OldRange) + NewMin
    print(newVal)
    return newVal

def gaugeDraw(newVal, oldVal, r, w, gaugeCenterX, gaugeCenterY, color):
    if newVal == oldVal:
        pass
    elif newVal > oldVal:
        print("newVal > oldVal")
        for i in range(oldVal, newVal):
            outerX = round(cos(radians(i)) * r) + gaugeCenterX
            outerY = round(sin(radians(i)) * r) + gaugeCenterY
            gaugeBmp[outerX,outerY] = color
            for q in range(w):
                x = round(cos(radians(i)) * (r-q)) + gaugeCenterX
                y = round(sin(radians(i)) * (r-q)) + gaugeCenterY
                gaugeBmp[x,y] = color
    elif newVal < oldVal:
        print("newVal < oldVal")
        for a in range(oldVal, newVal, -1):
            outerX = round(cos(radians(a)) * r) + gaugeCenterX
            outerY = round(sin(radians(a)) * r) + gaugeCenterY
            gaugeBmp[outerX,outerY] = 3
            print("OK?")
            for b in range(w):
                x = round(cos(radians(a)) * (r - b)) + gaugeCenterX
                y = round(sin(radians(a)) * (r - b)) + gaugeCenterY
                gaugeBmp[x,y] = 3

r = 70 #outer gauge radius
w = 20 #width of guage
firstRowX = 95
firstRowY = 95

rando2 = randint(179, 315)
rando3 = randint(180, 315)
rando4 = randint(189, 315)

for i in range(3):
    x = (firstRowX + (r*2*i))
    gaugeDraw(315, 180, r+4, w+4, x, firstRowY, 3)
    
while True:
    rando1 = randint(179, 315)
    for i in range(3):
        x = (firstRowX + (r*2*i))
        gaugeDraw(rando1, rando2, r, w, x, firstRowY, 1)
        rando2 = rando1
    sleep(1)
