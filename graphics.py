from math import *
from graphics import *
from time import *
from random import randint

win = GraphWin("TITANO",480,320)

	   
yCenter = 200
xCenter = 300
newVal = 360	  
oldVal = 180
r = 70
w = 50
arcWidth = r - w

def line(color, x0, y0, x1, y1, *args, **kwargs):
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
				pt = Point(y0,x0,*args,**kwargs)
				pt.setFill(color)
				pt.draw(win)

			else:
				pt = Point(x0,y0,*args,**kwargs)
				pt.setFill(color)
				pt.draw(win)

			err -= dy
			if err < 0:
				y0 += ystep
				err += dx
			x0 += 1
			
def arc(oldVal, newVal, r, w, yCenter, xCenter, color):
	outerYmax = round(sin(radians(newVal)) * r) + yCenter
	outerYmin = round(sin(radians(oldVal)) * r) + yCenter
	outerXmax = round(cos(radians(newVal)) * r ) + xCenter
	outerYcenter = round(sin(radians(270)) * r) + yCenter
	
	innerYmax = round(sin(radians(newVal)) * w) + yCenter
	innerXmax = round(cos(radians(newVal)) * w ) + xCenter
	innerYcenter = round(sin(radians(270)) * w) + yCenter
	innerYmin = round(sin(radians(newVal)) * w) + yCenter #past 270 degrees
	
	if newVal == oldVal:
		pass
	elif newVal > oldVal:
		if newVal > 270:
			innerYmax = innerYcenter
			outerYmax = outerYcenter
		# draw right arc
		for y in range(outerYmin, outerYmax, -1):
			print("outerYmax: " +str(outerYmax))
			print("outerYmin: " +str(outerYmin))
			print("innerYmax: " +str(innerYmax))
			print("Y1: " + str(y))
			if y > innerYmax:
				theta1 = asin((yCenter - y)/r)
				theta2 = asin((yCenter - y)/w)
				x1 = round(cos((theta1)) * r) + xCenter
				x2 = round(cos((theta2)) * w) + xCenter
				for x in range(x2, x1):
					pt = Point(x,y)
					pt.setFill(color)
					pt.draw(win)
				print("x1: " + str(x1))
				print("x2: " + str(x2))
			elif newVal > 270 and y < innerYmax:
				print("MIDDLE....................")
				theta1 = asin((yCenter - y)/r)
				x1 = round(cos((theta1)) * r) + xCenter
				print(x1)
				for x in range(x1, xCenter, -1):
					pt = Point(x,y)
					pt.setFill(color)
					pt.draw(win)
			elif innerYmax - outerYmax <= arcWidth: #this gives it a angle on the end of the arc instead of a horizontal line
				w += 1.5
				theta1 = asin((yCenter - y)/r)
				theta2 = asin((yCenter - y)/w)
				print("W: " + str(w))
				x1 = round(cos((theta1)) * r) + xCenter
				x2 = round(cos((theta2)) * w) + xCenter
				for x in range(x2, x1):
					pt = Point(x,y)
					pt.setFill(color)
					pt.draw(win)
				print("x1: " + str(x1))
				print("x2: " + str(x2))
		# Draw left arc
		if 270 < newVal <= 360:
			outerYmax = round(sin(radians(newVal)) * r ) + yCenter
			print("OUTERyMAX: " + str(outerYmax))
			print("INNERyMIN: " + str(innerYmin))
			for y in range(outerYcenter, innerYmin):
				print("Y: " + str(y))
				if y <= innerYcenter:
					theta1 = asin((yCenter - y)/r)
					x1 = xCenter - round(cos((theta1)) * r)
					for x in range(xCenter, x1, -1):
						pt = Point(x,y)
						pt.setFill(color)
						pt.draw(win)
				elif innerYcenter < y <= outerYmax:
					print("SWITCH")
					theta1 = asin((yCenter - y)/r)
					theta2 = asin((yCenter - y)/w)
					x1 = xCenter - round(cos(theta1) * r)
					x2 = xCenter - round(cos(theta2) * w)
					for x in range(x2, x1, -1):
						pt = Point(x,y)
						pt.setFill(color)
						pt.draw(win)
				elif outerYmax - innerYmin	<= arcWidth: 
					r -= 1.5
					theta1 = asin((yCenter - y)/r)
					theta2 = asin((yCenter - y)/w)
					x1 = xCenter - round(cos(theta1) * r)
					x2 = xCenter - round(cos(theta2) * w)
					print("x1: " +str(x1))
					print("x2: " +str(x2))
					for x in range(x2, x1, -1):
						pt = Point(x,y)
						pt.setFill(color)
						pt.draw(win)

		
#arc(oldVal, newVal, r+5, w-5, yCenter, xCenter, "blue")

def arc(newVal, oldVal, outer, inner, color):
	if newVal == oldVal:
		pass
	elif newVal > oldVal:
		for i in range(newVal,oldVal,-1):
				y = round(sin(radians(i)) * outer) + yCenter
				x = round(cos(radians(i)) * outer) + xCenter
				y2 = round(sin(radians(i)) * inner) + yCenter
				x2 = round(cos(radians(i)) * inner) + xCenter
				line("red", x2, y2, x, y)
	elif newVal < oldVal:
		for i in range(oldVal, newVal):
				y = round(sin(radians(i)) * outer) + yCenter
				x = round(cos(radians(i)) * outer) + xCenter
				y2 = round(sin(radians(i)) * inner) + yCenter
				x2 = round(cos(radians(i)) * inner) + xCenter
				line("red", x2, y2, x, y)
def line(color, x0, y0, x1, y1, *args, **kwargs):
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
				pt = Point(y0,x0,*args,**kwargs)
				pt.setFill(color)
				pt.draw(win)

			else:
				pt = Point(x0,y0,*args,**kwargs)
				pt.setFill(color)
				pt.draw(win)

			err -= dy
			if err < 0:
				y0 += ystep
				err += dx
			x0 += 1
			
yCenter = 200
xCenter = 300
r = 110
w = 90
r1 = 80
w1 = 40
while True:
	arc(newVal, oldVal, r, w, "purple")
	sleep(3)
	break
