from math import *
from graphics import *
from time import *

win = GraphWin("TITANO",480,320)
r = 70
w = 60
def line(x0, y0, x1, y1, *args, **kwargs):
	"""Line drawing function.  Will draw a single pixel wide line starting at
	x0, y0 and ending at x1, y1."""
	global win
	
	steep = abs(y1 - y0) > abs(x1 - x0)
	if steep:
		x0, y0 = y0, x0
		x1, y1 = y1, x1
	if x0 > x1:
		x0, x1 = x1, x0
		y0, y1 = y1, y0
	dx = x1 - x0
	dy = abs(y1 - y0)
	err = dx // 2
	ystep = 0
	if y0 < y1:
		ystep = 1
	else:
		ystep = -1
	while x0 <= x1:
		if steep:
			pt = Point(x0,y0)
			pt.draw(win)
		else:
			pt = Point(x0,y0)
			pt.draw(win)
		err -= dy
		if err < 0:
			y0 += ystep
			err += dx
		x0 += 1
		

def gaugeDraw(newVal, oldVal, r, w, gaugeCenterX, gaugeCenterY):
	if newVal == oldVal:
		pass
	elif newVal > oldVal:
		for i in range(oldVal, newVal):
			outerX = round(cos(radians(i)) * r) + gaugeCenterX
			outerY = round(sin(radians(i)) * r) + gaugeCenterY
			pt = Point(outerX,outerY)
			pt.draw(win)
			for q in range(1,w):
				x = round(cos(radians(i)) * (r-q)) + gaugeCenterX
				y = round(sin(radians(i)) * (r-q)) + gaugeCenterY
				pt = Point(x,y)
				pt.draw(win)
	elif newVal < oldVal:
		for a in range(oldVal, (newVal - 1), -1):
			outerX = round(cos(radians(a)) * r) + gaugeCenterX
			outerY = round(sin(radians(a)) * r) + gaugeCenterY
			pt = Point(outerX,outerY)
			pt.draw(win)
			for b in range(1,w):
				x = round(cos(radians(a)) * (r - b)) + gaugeCenterX
				y = round(sin(radians(a)) * (r - b)) + gaugeCenterY
				pt = Point(x,y)
				pt.draw(win)

previousLength = 0			
yCenter = 200
xCenter = 300
y = yCenter
while True:
	maxY = round(sin(radians(225)) * r ) + yCenter
	maxY2 = round(sin(radians(225)) * w) + wCenter
	minY = round(sin(radians(180)) * r) + yCenter
	maxAngle = asin((yCenter - maxY)/r)
	print(maxY)
	print(minY)
	sleep(1)
	previousLength = r-w	
	for y in range(minY, maxY, -1):
		theta1 = asin((yCenter - y)/r)
		theta2 = asin((yCenter - y)/w)
		print("W: " + str(w))
		x1 = round(cos((theta1)) * r) + xCenter
		x2 = round(cos((theta2)) * w) + xCenter
		l = x1 - x2
		print("L: " + str(l))
		if yCenter - y > w:
			w += 1
			print("SWITCH")
		for x in range(x2, x1):

			pt = Point(x,y)
			pt.draw(win)
		line(x1, y, x2, y)
		print("theta1: " + str(theta1))
		print("theta2: " + str(theta2))
		print("y: " + str(y))
		print("x1: " + str(x1))
		print("x2: " + str(x2))
		previousLength = l
	sleep(2)
	break

