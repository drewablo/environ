import board
import math
import displayio
import busio
import adafruit_sgp30
import adafruit_bme280
from math import cos
from math import sin
from math import radians
from time import time

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

display = board.DISPLAY
splash = displayio.Group(max_size=15)
 
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

eCO2Data = translate(sgp30.eCO2, TK, TK)
tvocData = translate(sgp30.TVOC, TK, TK)
tempData = bme280.temperature
# convert temperature (C-->F)
tempData = translate((int(tempData) * 1.8 + 32), TK, TK)
humidData = translate(bme280.humidity, TK, TK)
pressureData = translate(bme280.pressure, TK, TK)

tempPrevious = eCO2Data
humidPrevious = tvocData
pressurePrevious = tempData
eCO2Previous = humidData
tvocPrevious = pressureData

r = 30 #outer gauge radius
w = 10 #width of guage
class Timer:
    def __init__(self,timer_period):
        self.timer_period = timer_period
        self.update_timer()
    def update_timer(self):
        self.last_time = time()*100
        self.timer_expires = self.last_time + self.timer_period
    def has_timer_expired(self):
        if time()*100 > self.timer_expires:
            self.update_timer()
            return 1
        else:
            return 0

timer = Timer(5)

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
		for i in range(180, newVal, -1):
			outerX = round(cos(radians(i)) * r)
			outerY = round(sin(radians(i)) * r)
			gaugeBmp[(gaugeCenterX + outerX), (gaugeCenterY + outerY)] = 0
			for q in range(1,w):
				x = round(cos(radians(i)) * (r-q))
				y = round(sin(radians(i)) * (r-q))
				gaugeBmp[(gaugeCenterX + x), (gaugeCenterY + y)] = color
	elif newVal < oldVal:
		for a in range(oldVal, (newVal - 1), -1):
			outerX = round(cos(raidans(a)) * r)
			outerY = round(sin(radians(a)) * r)
			gaugeBmp[(gaugeCenterX + outerX), (gaugeCenterY + outerY)] = 0
			for b in range(1,w):
				x = round(cos(radians(a)) * (r - b))
				y = round(sin(radians(a)) * (r - b))
				gaugeBmp[(gaugeCenterX + x), (gaugeCenterY + y)] = 0
    else: 
        pass
	
gaugeDraw(90, 46, r+2, w+4, 40, 40, 4)
gaugeDraw(180, 91, r+2, w+4, 40, 40, 0)

while True:
	eCO2Data = translate(sgp30.eCO2, TK, TK)
	tvocData = translate(sgp30.TVOC, TK, TK)
	tempData = bme280.temperature
	# convert temperature (C-->F)
	tempData = translate((int(tempData) * 1.8 + 32), TK, TK)
	humidData = translate(bme280.humidity, TK, TK)
	pressureData = translate(bme280.pressure, TK, TK)
	
	if has_timer_expired():
        gaugeDraw(tempData, tempPrevious r, w, 40, 40, 1)
        gaugeDraw(humidData, humidPrevious,  r, w, 80, 80, 1)
        gaugeDraw(pressureData, pressurePrevious, r, w, 120, 120, 1)
        
        gaugeDraw(eCO2Data, eCO2Previous r, w, 100, 40, 1)
        gaugeDraw(tvocData, tvocPrevious r, w, 140, 80, 1)
	
	tempPrevious = eCO2Data
	humidPrevious = tvocData
	pressurePrevious = tempData
	eCO2Previous = humidData
	tvocPrevious = pressureData
