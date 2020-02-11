import board
import math
import displayio
import busio
import adafruit_sgp30
import adafruit_bme280

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

display = board.DISPLAY
splash = displayio.Group(max_size=15)
 
# Palette for gauge bitmap
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0x97f3e8
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

gaugeCenterX = 8
gaugeCenterY = 0

r = 60 #outer radius
w = 10 #width of guage

def translate(val, OldMin, OldMax, NewMin = 180, NewMax = 90):
	OldRange = (OldMax - OldMin)  
	NewRange = (NewMax - NewMin)  
	val = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	print(val)
	return val

def gaugeDraw(newVal, oldVal, r, w, gaugeCenterX, gaugeCenterY, color):
	if newVal > oldVal:
		for i in range(180, newVal):
			outerX = int(round(math.cos(i)*r))
			outerY = int(round(math.sin(i)*r))
			gaugeBmp[(gaugeCenterX + outerX), (gaugeCenterY + outerY)] = color
			for q in range(w):
				x = int(round(cos(i)*(r-q)))
				y = int(round(sin(i)*(r-q)))
				gaugeBmp[(gaugeCenterX + x), y] = color
	else:
		for _i in range(oldVal, (newVal - 1)):
			outerX = int(round(math.cos(_i)  r))
			outerY = int(round(math.sin(_i) * r))
			gaugeBmp[(gaugeCenterX + outerX), (gaugeCenterY + outerY)] = 0
			for _q in range(w):
				x = int(round(cos(_i)*(r - _q)))
				y = int(round(sin(_i)*(r - _q)))
				gaugeBmp[(gaugeCenterX + x), y] = 0
	
gaugeDraw(89, r+2, w+4, gaugeCenterX, 0)

while True:
	eCO2Data = translate(sgp30.eCO2, TK, TK)
	tvocData = translate(sgp30.TVOC, TK, TK)
	tempData = bme280.temperature
	# convert temperature (C-->F)
	tempData = translate((int(tempData) * 1.8 + 32), TK, TK)
	humidData = translate(bme280.humidity, TK, TK)
	pressureData = translate(bme280.pressure, TK, TK)
	
	if 
	
	gaugeDraw(tempData, r, w, 40, 40, 1)
	gaugeDraw(eCO2Data, r, w, 80, 80, 1)
	gaugeDraw(eCO2Data, r, w, 120, 120, 1)
	
	gaugeDraw(eCO2Data, r, w, 100, 40, 1)
	gaugeDraw(tvocData, r, w, 140, 80, 1)
	
	tempPrevious = eCO2Data
	humidPrevious = tvocData
	pressurePrevious = tempData
	eCO2Previous = humidData
	tvocPrevious = pressureData
		
	
	
-----------------------
from time import sleep
# generate random integer values
from random import seed
from random import randint
import math
# seed random number generator
seed(1)
# generate some integers

def translate(val, OldMin, OldMax, NewMin = 180, NewMax = 90):
	OldRange = (OldMax - OldMin)  
	NewRange = (NewMax - NewMin)  
	val = (((val - OldMin) * NewRange) / OldRange) + NewMin
	print(val)
	return val
	
def gaugeDraw(newVal, oldVal, r, w, gaugeCenterX, gaugeCenterY, color):
	if newVal > oldVal:
		for i in range(180, newVal, -1):
			outerX = int(math.cos(i)*r)
			outerY = int(math.sin(i)*r)
			print("A: " + str((gaugeCenterX + outerX)) + ", " + str((gaugeCenterY + outerY)))
			for q in range(1,w):
				x = int(math.cos(i)*(r-q))
				y = int(math.sin(i)*(r-q))
				print(str(gaugeCenterX + x) +", " + str(gaugeCenterY + y))
	else:
		for a in range(oldVal, (newVal - 1), -1):
			outerX = int(math.cos(a) * r)
			outerY = int(math.sin(a) * r)
			print(outerY)
			sleep(2)
			print("B: " + str((gaugeCenterX + outerX)) + ", " + str((gaugeCenterY + outerY)))
			for b in range(1,w):
				x = int(math.cos(a)*(r - b))
				y = int(math.sin(a)*(r - b))
				print(str(gaugeCenterX + x) +", " + str(gaugeCenterY + y))
	sleep(1)
for i in range(10):
	rando = randint(90, 180)
	rando2 = randint(90, 180)
	print("rando: "+str(rando))
	print("rando2: "+str(rando2))
	gaugeDraw(rando, rando2, 60, 10, 40, 40, 2)
	sleep(1)
	
	
