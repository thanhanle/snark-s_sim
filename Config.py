# math collision: https://www.topcoder.com/community/data-science/data-science-tutorials/geometry-concepts-line-intersection-and-its-applications/
# checklist: movement for ultrasound+car, inputs to car movement
# only 2 ouputs of neural network
# change in time measured in frames
# change in distance measured in pixels

import pygame
import time
import random
import math


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
acceleration = 0.2
decceleration = 0.2

def distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

def is_between(ax, ay, bx, by, cx, cy):
    return distance(ax, ay, cx, cy) + distance(cx, cy , bx, by) == distance(ax, ay, bx, by)