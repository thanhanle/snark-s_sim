from Config import*


class Ultrasound():
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