import pygame
import time
import random
import math
# math collision: https://www.topcoder.com/community/data-science/data-science-tutorials/geometry-concepts-line-intersection-and-its-applications/
# checklist: movement for ultrasound+car, inputs to car movement
# only 2 ouputs of neural network
# change in time measured in frames
# change in distance measured in pixels

# config
display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,255,0)
magenta = (255,0,255)
cyan = (0,255,255)
car_width = 25   	# 25x52
car_length = 52		# 25x52
num_obstacles = 1
obstacle_max_width = 50
obstacle_max_height = 50
obstacle_min_width = 20
obstacle_min_height = 20
ultrasound_length = 100
num_walls = 4 		# don't change

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
		#self.direction_vector = [0, 0]
		#self.center_vector = [0, 0]
		#self.left_vector = [0, 0]
		#self.right_vector = [0, 0]
		#self.center_acceleration_vector = [0, 0]
		#self.left_acceleration_vector = [0, 0]
		#self.right_acceleration_vector = [0, 0]
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
		max_frequency = 4.736 * wheel_Circ						# unit: pixels/frame (4.736 Hz): 4.736 * wheel_Circ/frame
		wheel_frequency1 = abs(output1) * max_frequency			# based on output: pixels per frame
		wheel_frequency2 = abs(output2) * max_frequency			# based on output: pixels per frame
		length1 = wheel_frequency1 * wheel_Circ * delta_frame 	# unit: pixels (cm)
		length2 = wheel_frequency2 * wheel_Circ * delta_frame	# unit: pixels (cm)

		# find the circle that the two outputs correspond to
		#radius = (length2 * car_width) / (length2 - length1)	# unit: pixels (cm)
		#angle = math.radians(length2 / radius)					# unit: ?????? (pixels/pixels = cm/cm ??????)

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
		rad = (lout * car_width) / (lout - lin)
		ang = math.radians(lout / rad)		

		if output1 > 0 and output2 > 0:
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
				#elif self.rightY == self.leftY:
				#	if self.rightX > self.leftX:
				#		circleX = self.leftX + rad
				#		circleY = self.rightY
				#		self.x_change(-circleX)
				#		self.y_change(-circleY)
				#		self.rotate(-ang)
				#		self.x_change(circleX)
				#		self.y_change(circleY)
				#		pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
				#	else:
				#		circleX = self.leftX - rad
				#		circleY = self.rightY
				#		self.x_change(-circleX)
				#		self.y_change(-circleY)
				#		self.rotate(-ang)
				#		self.x_change(circleX)
				#		self.y_change(circleY)
				#		pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
				#elif self.rightX == self.leftX:
				#	if self.rightY > self.leftY:
				#		circleX = self.leftX
				#		circleY = self.leftY + rad
				#		self.x_change(-circleX)
				#		self.y_change(-circleY)
				#		self.rotate(-ang)
				#		self.x_change(circleX)
				#		self.y_change(circleY)
				#		pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
				#	else:
				#		circleX = self.leftX 
				#		circleY = self.leftY - rad
				#		self.x_change(-circleX)
				#		self.y_change(-circleY)
				#		self.rotate(-ang)
				#		self.x_change(circleX)
				#		self.y_change(circleY)
				#		pygame.draw.circle(gameDisplay, color, [int(circleX), int(circleY)], int(rad), 1)
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
				#elif self.rightY == self.leftY:
				#	if self.rightX > self.leftX:
				#		pass
				#	else:
				#		pass
				#elif self.rightX == self.leftX:
				#	if self.rightY > self.leftY:
				#		pass
				#	else:
				#		pass
			elif output1 == output2:
				pass
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
			elif output1 == output2:
				pass
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
		ultra1 = Ultrasoud(self.x0+0.5*car_width, self.y0, self.x0, self.y0-ultrasound_length, self.x0+car_width, self.y0-ultrasound_length, 1)
		ultra2 = Ultrasoud(self.x0+0.5*car_width, self.y0+car_length, self.x0,self.y0+car_length+ultrasound_length, self.x0+car_width,self.y0+car_length+ultrasound_length, 2)
		ultra3 = Ultrasoud(self.x0, self.y0+0.33*car_length, self.x0-ultrasound_length, self.y0+0.33*car_length+0.5*car_width, self.x0-ultrasound_length,self.y0+0.33*car_length-0.5*car_width, 3)
		ultra4 = Ultrasoud(self.x0, self.y0+0.66*car_length, self.x0-ultrasound_length,self.y0+0.66*car_length+0.5*car_width, self.x0-ultrasound_length,self.y0+0.66*car_length-0.5*car_width, 4)
		ultra5 = Ultrasoud(self.x0+car_width,self.y0+0.66*car_length, self.x0+ultrasound_length+car_width, self.y0+0.66*car_length+0.5*car_width, self.x0+ultrasound_length+car_width,self.y0+0.66*car_length-0.5*car_width, 5)
		ultra6 = Ultrasoud(self.x0+car_width,self.y0+0.33*car_length, self.x0+ultrasound_length+car_width, self.y0+0.33*car_length+0.5*car_width, self.x0+ultrasound_length+car_width,self.y0+0.33*car_length-0.5*car_width, 6)
		self.ultrasound_list.append(ultra1)
		self.ultrasound_list.append(ultra2)
		self.ultrasound_list.append(ultra3)
		self.ultrasound_list.append(ultra4)
		self.ultrasound_list.append(ultra5)
		self.ultrasound_list.append(ultra6)

def distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

def is_between(ax, ay, bx, by, cx, cy):
    return distance(ax, ay, cx, cy) + distance(cx, cy , bx, by) == distance(ax, ay, bx, by)

class Ultrasoud():
	def __init__(self, x0, y0, x1, y1, x2, y2, ultrasound_num):
		self.ultrasound_num = ultrasound_num
		self.x0 = x0
		self.y0 = y0
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
	# function does math collision b/w ultrasound and obstacles
	def add_lineSeg_distance(self, list_distances, x0, y0, x1, y1, x2, y2, x3, y3):
		A1 = y1 - y0
		B1 = x0 - x1
		C1 = A1*x0 + B1*y0
		A2 = y3 - y2
		B2 = x2 - x3
		C2 = A2*x2 + B2*y2
		denominator = A1*B2 - A2*B1
		# if parallel
		if denominator == 0:
			return  
		else:
			x = (B2*C1 - B1*C2)/denominator
			y = (A1*C2 - A2*C1)/denominator
			# check and break or append to list based on results
			if (x >= min(x0, x1) and x <= max(x0, x1) and y >= min(y0, y1) and y <= max(y0, y1)) and (x >= min(x2, x3) and x <= max(x2, x3) and y >= min(y2, y3) and y <= max(y2, y3)):
				pygame.draw.circle(gameDisplay, blue, [int(x), int(y)], 10, 1)
				list_distances.append(distance(self.x0, self.y0, x, y))
	def x_change(self, x):
		self.x0 = self.x0 + x
		self.x1 = self.x1 + x
		self.x2 = self.x2 + x
	def y_change(self, y):
		self.y0 = self.y0 + y
		self.y1 = self.y1 + y
		self.y2 = self.y2 + y
	def rotate(self, angle):
		self.x0 = self.x0 * math.cos(angle) - self.y0 * math.sin(angle)
		self.x1 = self.x1 * math.cos(angle) - self.y1 * math.sin(angle)
		self.x2 = self.x2 * math.cos(angle) - self.y2 * math.sin(angle)
		self.y0 = self.x0 * math.sin(angle) + self.y0 * math.cos(angle)
		self.y1 = self.x1 * math.sin(angle) + self.y1 * math.cos(angle)
		self.y2 = self.x2 * math.sin(angle) + self.y2 * math.cos(angle)
	def read(self, obstacle_list):
		list_distances = []
		for obstacle in obstacle_list:
			self.add_lineSeg_distance(list_distances, self.x0, self.y0, self.x1, self.y1, obstacle.x0, obstacle.y0, obstacle.x1, obstacle.y1)
			self.add_lineSeg_distance(list_distances, self.x0, self.y0, self.x1, self.y1, obstacle.x1, obstacle.y1, obstacle.x2, obstacle.y2)
			self.add_lineSeg_distance(list_distances, self.x0, self.y0, self.x1, self.y1, obstacle.x2, obstacle.y2, obstacle.x3, obstacle.y3)
			self.add_lineSeg_distance(list_distances, self.x0, self.y0, self.x1, self.y1, obstacle.x3, obstacle.y3, obstacle.x0, obstacle.y0)
			self.add_lineSeg_distance(list_distances, self.x1, self.y1, self.x2, self.y2, obstacle.x0, obstacle.y0, obstacle.x1, obstacle.y1)
			self.add_lineSeg_distance(list_distances, self.x1, self.y1, self.x2, self.y2, obstacle.x1, obstacle.y1, obstacle.x2, obstacle.y2)
			self.add_lineSeg_distance(list_distances, self.x1, self.y1, self.x2, self.y2, obstacle.x2, obstacle.y2, obstacle.x3, obstacle.y3)
			self.add_lineSeg_distance(list_distances, self.x1, self.y1, self.x2, self.y2, obstacle.x3, obstacle.y3, obstacle.x0, obstacle.y0)
			self.add_lineSeg_distance(list_distances, self.x2, self.y2, self.x0, self.y0, obstacle.x0, obstacle.y0, obstacle.x1, obstacle.y1)
			self.add_lineSeg_distance(list_distances, self.x2, self.y2, self.x0, self.y0, obstacle.x1, obstacle.y1, obstacle.x2, obstacle.y2)
			self.add_lineSeg_distance(list_distances, self.x2, self.y2, self.x0, self.y0, obstacle.x2, obstacle.y2, obstacle.x3, obstacle.y3)
			self.add_lineSeg_distance(list_distances, self.x2, self.y2, self.x0, self.y0, obstacle.x3, obstacle.y3, obstacle.x0, obstacle.y0)
		if len(list_distances) == 0:
			print(str(self.ultrasound_num) + ": no collision")
		else:
			print(str(self.ultrasound_num) + ": " + str(min(list_distances)))
	def draw(self, gameDisplay, color):
		pygame.draw.lines(gameDisplay, color, True, [(self.x0,self.y0), (self.x1,self.y1), (self.x2,self.y2)], 1)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# --------------------
# 		SPAWNING
# --------------------
# spawn WALLS
wall1 = Rectangle(0, 0, display_width, 10)
wall2 = Rectangle(0, display_height-10, display_width, 10)
wall3 = Rectangle(0, 10, 10, display_height-20)
wall4 = Rectangle(display_width-10, 10, 10, display_height-20)
obstacles = [wall1, wall2, wall3, wall4]
# spawn OBSTACLES
for i in range(num_obstacles):
	x0 = random.randint(0, display_width)
	y0 = random.randint(0, display_height)
	obstacle_width = random.randint(obstacle_min_width, obstacle_max_width)
	obstacle_height = random.randint(obstacle_min_height, obstacle_max_height)
	obstacle = Rectangle(x0, y0, obstacle_width, obstacle_height)
	check = 0
	while check < len(obstacles):
		check = 0
		for x in obstacles:
			if obstacle.poly_collides_rect(x):
				x0 = random.randint(0, display_width)
				y0 = random.randint(0, display_height)
				obstacle_width = random.randint(obstacle_min_width, obstacle_max_width)
				obstacle_height = random.randint(obstacle_min_height, obstacle_max_height)
				obstacle = Rectangle(x0, y0, obstacle_width, obstacle_height)
			else:
				check = check + 1
	obstacles.append(obstacle)
# spawn CAR
car = Rectangle(random.randint(10, display_width-10-car_width), random.randint(10, display_height-10-car_length), car_width, car_length)
check = 0
while check < len(obstacles):
	check = 0
	for x in obstacles:
		if car.poly_collides_rect(x):
			car = Rectangle(random.randint(10, display_width-10-car_width), random.randint(10, display_height-10-car_length), car_width, car_length)
		else:
			check = check + 1
# spawn ULTRASOUNDS
car.spawn_ultrasounds()

# game logic
def game_loop():

	x_change = 0
	y_change = 0
	gameExit = False
	frame = 0
	delta_frame = 0

	while not gameExit:
		frame = frame + 1
		delta_frame = delta_frame + 1

		# for event per frame
		#for event in pygame.event.get():
		#	if event.type == pygame.QUIT:
		#		gameExit = True
		#	if event.type == pygame.KEYDOWN:
		#		if event.key == pygame.K_LEFT:
		#			x_change = -5
		#		if event.key == pygame.K_RIGHT:
		#			x_change = 5
		#		if event.key == pygame.K_UP:
		#			y_change = -5
		#		if event.key == pygame.K_DOWN:
		#			y_change = 5
		#	if event.type == pygame.KEYUP:
		#		if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or pygame.K_DOWN or pygame.K_UP:
		#			x_change = 0
		#			y_change = 0
		#car.x_change(x_change)
		#car.y_change(y_change)

		# debug
		event_debugger = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -5
				if event.key == pygame.K_RIGHT:
					x_change = 5
				if event.key == pygame.K_UP:
					y_change = -5
				if event.key == pygame.K_DOWN:
					y_change = 5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or pygame.K_DOWN or pygame.K_UP:
					x_change = 0
					y_change = 0
		#car.x_change(x_change)
		#car.y_change(y_change)
		#car.car_move(0.9, 0.8, .05, gameDisplay, yellow)

		# check for collisions and draw obstacles
		gameDisplay.fill(white)
		for x in obstacles:
			x.draw_obstacle(gameDisplay, black)
			if car.poly_collides_rect(x):
				gameExit = True

		car.car_move(-0.8, -0.9, .05, gameDisplay, yellow)
		#car.car_move(-0.9, -0.8, .05, gameDisplay, yellow)
		# draw updated car + ultrasound
		car.draw_car(gameDisplay, red)

		# print ultrasound readings
		for ultrasound in car.ultrasound_list:
			ultrasound.read(obstacles)

		pygame.display.update()
		clock.tick(20)



# main logic
game_loop()
pygame.quit()
quit()    
                      