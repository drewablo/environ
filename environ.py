import board
import displayio
import busio
import adafruit_sgp30
import adafruit_dht
from adafruit_display_shapes.rect import Rect
from math import cos
from math import sin
from math import radians
from time import time
from time import sleep
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

cwd = ("/"+__file__).rsplit('/', 1)[0]
font = bitmap_font.load_font(cwd+"/fonts/Noto-18.bdf")
font.load_glyphs("0123456789.TVOCeC".encode('utf-8'))

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

dht = adafruit_dht.DHT11(board.D2)
temperature = dht.temperature
humidity = dht.humidity

display = board.DISPLAY
splash = displayio.Group(max_size=75)

# Background
BGbitmap = displayio.Bitmap(display.width, display.height, 1)
BGpalette = displayio.Palette(1)
BGpalette[0] = 0x28565b
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

r = 110 #outer gauge radius
w = 30 #width of guage

def textDisplay(displayString, displayFont, xLoc, yLoc, textColor, screen):
    displayText = Label(displayFont, text=displayString)
    displayText.x = xLoc
    displayText.y = yLoc
    displayText.color = textColor
    screen.append(displayText)
    
def translate(val, OldMin, OldMax, NewMin, NewMax):
    OldRange = (OldMax - OldMin)
    NewRange = (NewMax - NewMin)
    newVal = int((((val - OldMin) * NewRange) / OldRange) + NewMin)
    return newVal

def setBacklight(val):
    val = max(0, min(1.0, val))
    board.DISPLAY.auto_brightness = False
    board.DISPLAY.brightness = val 

def textUpdate(sensorName):
	splash.pop()
	splash.pop()
	if sensorName == eCO2:
		textDisplay(str(sgp30.eCO2), font, firstRowX, firstRowY-10, 0x000000, splash)
	elif sensorName == TVOC:
		textDisplay(str(sgp30.TVOC), font, firstRowX+2*r+10, firstRowY-10, 0x000000, splash)
	elif sensorName == temp:
		textDisplay(str(sgp30.eCO2), font, secondRowX, secondRowX-10, 0x000000, splash)
	elif sensorName == humid:
		textDisplay(str(sgp30.TVOC), font, secondRowX+2*r+10, secondRowY-10, 0x000000, splash)	
		
def gaugeDraw(sensorName, newVal, oldVal, r, w, gaugeCenterX, gaugeCenterY, color, setUp = False):
	totalDegrees = newVal - oldVal
	if newVal == oldVal:
		pass
	elif newVal > oldVal:
		if setUP == False:
			textUpdate(sensorName)
		for i in range(r):
			x1 = round(cos(totalDegrees - i) * r) + gaugeCenterX
			x2 = round(cos(totalDegrees - i) * w) + gaugeCenterX
			y = gaugeCenterY + i
			for q in range(x1, x2):
				x = x1+q
				gaugeBmp[x,y] = color
	elif newVal > oldVal:
		if setUP == False:
			textUpdate(sensorName)
		for a in range(r):
				x1 = round(cos(totalDegrees - a) * r) + gaugeCenterX
				x2 = round(cos(totalDegrees - a) * w) + gaugeCenterX
				y = gaugeCenterY + i
				for b in range(x1, x2):
					x = x1+b
					gaugeBmp[x,y] = color


firstRowX = 130
firstRowY = 250
secondRowX = 130
firstRowY = 130
gaugeMax = 315
gaugeMin = 180
eCO2Data = translate(sgp30.eCO2, 400, 60000, gaugeMin, gaugeMax)
tvocData = translate(sgp30.TVOC, 0, 20000, gaugeMin, gaugeMax)
tempData = translate(temperature, -10, 50, gaugeMin, gaugeMax)
humidData = translate(humidity, 0, 100, gaugeMin, gaugeMax)
eCO2Previous = eCO2Data
tvocPrevious = tvocData
tempPrevious = temperature
humidPrevious = humidity
setBacklight(0.75)

rect1a = Rect(firstRowX-r-4, firstRowY, r*2-10, 2, fill=0x000000)
rect1b = Rect(firstRowX+r-15, firstRowY-r, 8, r+2, fill=0x000000)
rect2a = Rect(firstRowX+r*2+6-r, firstRowY, r*2-10, 2, fill=0x000000)
rect2b = Rect(firstRowX+3*r-5, firstRowY-r, 8, r+2, fill=0x000000)
splash.append(rect1a)
splash.append(rect1b)
splash.append(rect2a)
splash.append(rect2b)
rect3a = Rect(secondRowX-r-4, secondRowY, r*2-10, 2, fill=0x000000)
rect3b = Rect(secondRowX+r-15, secondRowY-r, 8, r+2, fill=0x000000)
rect4a = Rect(secondRowX+r*2+6-r, secondRowY, r*2-10, 2, fill=0x000000)
rect5b = Rect(secondRowX+3*r-5, secondRowY-r, 8, r+2, fill=0x000000)
splash.append(rect3a)
splash.append(rect3b)
splash.append(rect4a)
splash.append(rect4b)

for i in range(2):
    x = (firstRowX + ((r*2+10)*i))
    gaugeDraw(gaugeMax, gaugeMin, r+4, w+4, x, firstRowY, 3, True)
    gaugeDraw(317/coveragePercent, 315, r+15, w+30, x, firstRowY, 3, True)
for j in range(2):
    x = (secondRowX + ((r*2+10)*j))
    gaugeDraw(gaugeMax, gaugeMin, r+4, w+4, x, secondRowY, 3, True)
    gaugeDraw(317/coveragePercent, 315, r+15, w+30, x, secondRowY, 3, True)
for k in range(2):
    x = (firstRowX + ((r*2+10)*k))
    gaugeDraw(gaugeMax,gaugeMin, r, w-4, x, firstRowY, 1, True)
    gaugeDraw(gaugeMin,gaugeMax, r, w-4, x, firstRowY, 1, True)
for l in range(2):
    x = (secondRowX + ((r*2+10)*l))
    gaugeDraw(gaugeMax,gaugeMin, r, w-4, x, secondRowY, 1, True)
    gaugeDraw(gaugeMin,gaugeMax, r, w-4, x, secondRowY, 1, True)
	
textDisplay("eCO2", font, firstRowX-r, firstRowY+20, 0x000000, splash)
textDisplay("TVOC", font, firstRowX+10+r, firstRowY+20, 0x000000, splash)
condition = Rect(firstRowX-r-4, 20, 160, 70, fill=0x000000)
condition2 = Rect(firstRowX+60, 20, 275, 70, fill=0x000000)
splash.append(condition)
splash.append(condition2)
textDisplay(str(sgp30.eCO2), font, firstRowX, firstRowY-10, 0x000000, splash)
textDisplay(str(sgp30.TVOC), font, firstRowX+2*r+10, firstRowY-10, 0x000000, splash)

while True:
    print("eCO2: " + str(sgp30.eCO2))
    print("tvoc: " + str(sgp30.TVOC))
    eCO2Data = translate(sgp30.eCO2, 400, 60000, gaugeMin, gaugeMax)
    tvocData = translate(sgp30.TVOC, 0, 20000, gaugeMin, gaugeMax)
	tempData = translate(temperature, -10, 50, gaugeMin, gaugeMax)
	humidData = translate(humidity, 0, 100, gaugeMin, gaugeMax)
    gaugeDraw("eCO2", eCO2Data, eCO2Previous, r, w-4, firstRowX, firstRowY, 1)
    gaugeDraw("TVOC", tvocData, tvocPrevious, r, w-4, (firstRowX+(r*2+10)), firstRowY, 1)
	gaugeDraw("temp", tempData, tempPrevious, r, w-4, secondRowX, secondRowY, 1)
	gaugeDraw("humid", humidData, humidPrevious, r, w-4, (secondRowX+(r*2+10)), secondRowY, 1)
    sleep(.5)
    eCO2Previous = eCO2Data
    tvocPrevious = tvocData
	tempPrevious = tempData
	humidPrevious = humidData
