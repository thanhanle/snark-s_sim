from Rectangle import*


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

car.car_move(-0.09, -0.1, .05, gameDisplay, yellow)



# --------------------
# 		GAME LOGIC
# --------------------
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

		car.car_move(-0.01, -0.01, .05, gameDisplay, yellow)
		#car.car_move(-0.9, -0.8, .05, gameDisplay, yellow)
		# draw updated car + ultrasound
		car.draw_car(gameDisplay, red)

		# print ultrasound readings
		for ultrasound in car.ultrasound_list:
			ultrasound.read(obstacles)

		pygame.display.update()
		clock.tick(20)



# --------------------
# 		MAIN LOGIC
# --------------------
game_loop()
pygame.quit()
quit()    