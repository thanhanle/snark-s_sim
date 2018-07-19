from Ultrasound import*


# class is used for both obstacles with additional variables + functions for car
class Rectangle():
	def __init__(self, x0, y0, width, height):
		# obstacle
		self.x0 = x0
		self.y0 = y0
		self.x1 = x0+width
		self.y1 = y0
		self.x2 = x0+width
		self.y2 = y0+height
		self.x3 = x0
		self.y3 = y0+height
		self.width = width
		self.height = height
		# extra for car
		self.ultrasound_list = []
		self.centerX = x0+0.5*width
		self.centerY = y0+0.5*height
		self.frontX = self.centerX
		self.frontY = self.centerY + 0.5*car_length
		self.leftX = self.x0 
		self.leftY = self.y0 + 0.5*car_length
		self.rightX = self.x1 
		self.rightY = self.y1 + 0.5*car_length
	def draw_car(self, gameDisplay, color):
		pygame.draw.lines(gameDisplay, color, True, [(self.x0,self.y0), (self.x1,self.y1), (self.x2,self.y2), (self.x3,self.y3)], 1)
		for ultra in self.ultrasound_list:
			ultra.draw(gameDisplay,green)
		pygame.draw.circle(gameDisplay, red, [int(self.frontX), int(self.frontY)], 5, 1)
		pygame.draw.circle(gameDisplay, cyan, [int(self.rightX), int(self.rightY)], 5, 1)
	def draw_obstacle(self, gameDisplay, color):
		pygame.draw.lines(gameDisplay, color, True, [(self.x0,self.y0), (self.x1,self.y1), (self.x2,self.y2), (self.x3,self.y3)], 1)
	def rect_collides_rect(self, obstacle):
		if ((self.x0 >= obstacle.x0 and self.x0 <= obstacle.x1 and self.y0 >= obstacle.y0 and self.y0 <= obstacle.y3) or (self.x2 >= obstacle.x0 and self.x2 <= obstacle.x1 and self.y2 >= obstacle.y0 and self.y2 <= obstacle.y3) or 
		(obstacle.x0 >= self.x0 and obstacle.x0 <= self.x1 and obstacle.y0 >= self.y0 and obstacle.y0 <= self.y3) or (obstacle.x2 >= self.x0 and obstacle.x2 <= self.x1 and obstacle.y2 >= self.y0 and obstacle.y2 <= self.y3)):
			return True
		return False
	def poly_collides_rect(self, obstacle):
		if ((self.x0 >= obstacle.x0 and self.x0 <= obstacle.x1 and self.y0 >= obstacle.y0 and self.y0 <= obstacle.y3) or (self.x1 >= obstacle.x0 and self.x1 <= obstacle.x1 and self.y1 >= obstacle.y0 and self.y1 <= obstacle.y3) or (self.x2 >= obstacle.x0 and self.x2 <= obstacle.x1 and self.y2 >= obstacle.y0 and self.y2 <= obstacle.y3) or (self.x3 >= obstacle.x0 and self.x3 <= obstacle.x1 and self.y3 >= obstacle.y0 and self.y3 <= obstacle.y3) or
		(obstacle.x0 >= self.x0 and obstacle.x0 <= self.x1 and obstacle.y0 >= self.y0 and obstacle.y0 <= self.y3) or (obstacle.x1 >= self.x0 and obstacle.x1 <= self.x1 and obstacle.y1 >= self.y0 and obstacle.y1 <= self.y3) or (obstacle.x2 >= self.x0 and obstacle.x2 <= self.x1 and obstacle.y2 >= self.y0 and obstacle.y2 <= self.y3) or (obstacle.x3 >= self.x0 and obstacle.x3 <= self.x1 and obstacle.y3 >= self.y0 and obstacle.y3 <= self.y3)):
			return True
		return False
	# change
	def car_move(self, output1, output2, delta_frame, gameDisplay, color):
		max_velocity = 118.4062519								# unit: pixels/frame (100 m/s)
		wheel_Circ = 25    										# unit: pixels (21.11375 cm)    NOTE: every 21.11375 cm = 25 pixels
		wheel_Rad = wheel_Circ / (2*math.pi)
		#max_frequency = 4.736 * wheel_Circ						# unit: pixels/frame (4.736 Hz): 4.736 * wheel_Circ/frame
		max_frequency = 4.736 * wheel_Circ						# unit: pixels/frame (4.736 Hz): 4.736 * wheel_Circ/frame
		wheel_frequency1 = abs(output1) * max_frequency			# based on output: pixels per frame
		wheel_frequency2 = abs(output2) * max_frequency			# based on output: pixels per frame
		length1 = wheel_frequency1 * wheel_Circ * delta_frame 	# unit: pixels (cm)
		length2 = wheel_frequency2 * wheel_Circ * delta_frame	# unit: pixels (cm)

		if output1 != output2:	
			lin = 0
			lout = 0 
			rad = 0
			ang = 0
			if abs(output1) > abs(output2):
				lout = length1
				lin = length2
			elif abs(output1) < abs(output2):
				lout = length2
				lin = length1
			# find the circle that the two outputs correspond to using the radius and angle calculated
			rad = (lout * car_width) / (lout - lin)					# unit: pixels (cm)
			ang = math.radians(lout / rad)							# unit: ?????? (pixels/pixels = cm/cm ??????)

		if output1 == output2:
			distance = 2 * math.pi * wheel_frequency1 * wheel_Rad * delta_frame
			if self.x2 > self.x1 and self.y2 > self.y1:	
				ang_tan = math.atan((self.y2-self.y1)/(self.x2-self.x1))
				if output1 > 0:
					self.x_change(math.cos(ang_tan) * distance)
					self.y_change(math.tan(ang_tan) * distance)
				else:
					self.x_change(math.cos(ang_tan) * distance * -1)
					self.y_change(math.tan(ang_tan) * distance * -1)
			elif self.x2 < self.x1 and self.y2 > self.y1:
				ang_tan = math.atan((self.y2-self.y1)/(self.x1-self.x2))
				if output1 > 0:
					self.x_change(math.cos(ang_tan) * distance * -1)
					self.y_change(math.tan(ang_tan) * distance)
				else:
					self.x_change(math.cos(ang_tan) * distance)
					self.y_change(math.tan(ang_tan) * distance * -1)
			elif self.x2 > self.x1 and self.y2 < self.y1:
				ang_tan = math.atan((self.y1-self.y2)/(self.x2-self.x1))
				if output1 > 0:
					self.x_change(math.cos(ang_tan) * distance)
					self.y_change(math.tan(ang_tan) * distance * -1)
				else:
					self.x_change(math.cos(ang_tan) * distance * -1)
					self.y_change(math.tan(ang_tan) * distance)
			elif self.x2 < self.x1 and self.y2 < self.y1:
				ang_tan = math.atan((self.y1-self.y2)/(self.x1-self.x2))
				if output1 > 0:
					self.x_change(math.cos(ang_tan) * distance * -1)
					self.y_change(math.tan(ang_tan) * distance * -1)
				else:
					self.x_change(math.cos(ang_tan) * distance)
					self.y_change(math.tan(ang_tan) * distance)
			elif self.x2 == self.x1 and self.y2 < self.y1:
				if output1 > 0:
					self.y_change(-distance)
				else:
					self.y_change(distance)
			elif self.x2 == self.x1 and self.y2 > self.y1:
				if output1 > 0:
					self.y_change(distance)
				else:
					self.y_change(-distance)
			elif self.x2 < self.x1 and self.y2 == self.y1:
				if output1 > 0:
					self.x_change(-distance)
				else:
					self.x_change(distance)
			elif self.x2 > self.x1 and self.y2 == self.y1:
				if output1 > 0:
					self.x_change(distance)
				else:
					self.x_change(-distance)
			elif output1 == 0 and output2 == 0:
				return
		elif output1 > 0 and output2 > 0:
			if output1 > output2:
				if self.rightX > self.leftX or self.rightX < self.leftX:   											
					circleX = self.leftX + rad * ((self.rightX - self.leftX) / car_width)
					circleY = self.leftY + rad * ((self.rightY - self.leftY) / car_width)
					# translate points /w respect to origin
					self.x_change(-circleX)
					self.y_change(-circleY)
					# rotate points
					self.rotate(-ang)
					# translate points back
					self.x_change(circleX)
					self.y_change(circleY)
					pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
			elif output1 < output2:
				if self.rightX > self.leftX or self.rightX < self.leftX:   											
					circleX = self.rightX + rad * ((self.leftX - self.rightX) / car_width)
					circleY = self.rightY + rad * ((self.leftY - self.rightY) / car_width)
					self.x_change(-circleX)
					self.y_change(-circleY)
					self.rotate(ang)
					self.x_change(circleX)
					self.y_change(circleY)
					pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
		elif output1 < 0 and output2 < 0:
			if abs(output1) > abs(output2):
				if self.rightX > self.leftX or self.rightX < self.leftX:   		
					circleX = self.leftX + rad * ((self.rightX - self.leftX) / car_width)
					circleY = self.leftY + rad * ((self.rightY - self.leftY) / car_width)								
					self.x_change(-circleX)
					self.y_change(-circleY)
					self.rotate(ang)
					self.x_change(circleX)
					self.y_change(circleY)
					pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
			elif abs(output1) < abs(output2):
				if self.rightX > self.leftX or self.rightX < self.leftX:   											
					circleX = self.rightX + rad * ((self.leftX - self.rightX) / car_width)
					circleY = self.rightY + rad * ((self.leftY - self.rightY) / car_width)
					self.x_change(-circleX)
					self.y_change(-circleY)
					self.rotate(-ang)
					self.x_change(circleX)
					self.y_change(circleY)
					pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
		elif output1 < 0 and output2 > 0:
			pass
		elif output1 > 0 and output2 < 0:
			pass

	def x_change(self, x):
		self.x0 = self.x0 + x
		self.x1 = self.x1 + x
		self.x2 = self.x2 + x
		self.x3 = self.x3 + x
		self.frontX = self.frontX + x
		self.centerX = self.centerX + x
		self.leftX = self.leftX + x
		self.rightX = self.rightX + x
		for ultra in self.ultrasound_list:
			ultra.x_change(x)
	def y_change(self, y):
		self.y0 = self.y0 + y
		self.y1 = self.y1 + y
		self.y2 = self.y2 + y
		self.y3 = self.y3 + y
		self.frontY = self.frontY + y
		self.centerY = self.centerY + y
		self.leftY = self.leftY + y
		self.rightY = self.rightY + y
		for ultra in self.ultrasound_list:
			ultra.y_change(y)
	def rotate(self, angle):
		# move x
		self.x0 = self.x0 * math.cos(angle) - self.y0 * math.sin(angle)
		self.x1 = self.x1 * math.cos(angle) - self.y1 * math.sin(angle)
		self.x2 = self.x2 * math.cos(angle) - self.y2 * math.sin(angle)
		self.x3 = self.x3 * math.cos(angle) - self.y3 * math.sin(angle)
		self.frontX = self.frontX * math.cos(angle) - self.frontY * math.sin(angle)
		self.centerX = self.centerX * math.cos(angle) - self.centerY * math.sin(angle)
		self.leftX = self.leftX * math.cos(angle) - self.leftY * math.sin(angle)
		self.rightX = self.rightX * math.cos(angle) - self.rightY * math.sin(angle)
		# move y
		self.y0 = self.x0 * math.sin(angle) + self.y0 * math.cos(angle)
		self.y1 = self.x1 * math.sin(angle) + self.y1 * math.cos(angle)
		self.y2 = self.x2 * math.sin(angle) + self.y2 * math.cos(angle)
		self.y3 = self.x3 * math.sin(angle) + self.y3 * math.cos(angle)
		self.frontY = self.frontX * math.sin(angle) + self.frontY * math.cos(angle)
		self.centerY = self.centerX * math.sin(angle) + self.centerY * math.cos(angle)
		self.leftY = self.leftX * math.sin(angle) + self.leftY * math.cos(angle)
		self.rightY = self.rightX * math.sin(angle) + self.rightY * math.cos(angle)
		# move ultrasounds
		for ultra in self.ultrasound_list:
			ultra.rotate(angle)
	def spawn_ultrasounds(self):
		ultra1 = Ultrasound(self.x0+0.5*car_width, self.y0, self.x0, self.y0-ultrasound_length, self.x0+car_width, self.y0-ultrasound_length, 1)
		ultra2 = Ultrasound(self.x0+0.5*car_width, self.y0+car_length, self.x0,self.y0+car_length+ultrasound_length, self.x0+car_width,self.y0+car_length+ultrasound_length, 2)
		ultra3 = Ultrasound(self.x0, self.y0+0.33*car_length, self.x0-ultrasound_length, self.y0+0.33*car_length+0.5*car_width, self.x0-ultrasound_length,self.y0+0.33*car_length-0.5*car_width, 3)
		ultra4 = Ultrasound(self.x0, self.y0+0.66*car_length, self.x0-ultrasound_length,self.y0+0.66*car_length+0.5*car_width, self.x0-ultrasound_length,self.y0+0.66*car_length-0.5*car_width, 4)
		ultra5 = Ultrasound(self.x0+car_width,self.y0+0.66*car_length, self.x0+ultrasound_length+car_width, self.y0+0.66*car_length+0.5*car_width, self.x0+ultrasound_length+car_width,self.y0+0.66*car_length-0.5*car_width, 5)
		ultra6 = Ultrasound(self.x0+car_width,self.y0+0.33*car_length, self.x0+ultrasound_length+car_width, self.y0+0.33*car_length+0.5*car_width, self.x0+ultrasound_length+car_width,self.y0+0.33*car_length-0.5*car_width, 6)
		self.ultrasound_list.append(ultra1)
		self.ultrasound_list.append(ultra2)
		self.ultrasound_list.append(ultra3)
		self.ultrasound_list.append(ultra4)
		self.ultrasound_list.append(ultra5)
		self.ultrasound_list.append(ultra6)