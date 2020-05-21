import curses
from curses import wrapper
import os 
import random

"""
Works, but needs a lot of touch up and improvements, pass through walls, speed up with 
length, etc.
"""

class Field():
	def __init__(self):
		self.f = curses.newwin(0,0)

class Snake():
	def __init__(self, length, field):
		self.l = length
		self.f = field
		self.startingX = 0
		self.startingY = 0
		self.head = []
		self.direction = "dUp"
		self.last = []
		self.blast = []
	
	def construct(self):
		self.startingX = round(self.f.f.getmaxyx()[1]/2)
		self.startingY = round(self.f.f.getmaxyx()[0]/2)
		self.head = [[self.startingY, self.startingX]]

	def move(self):
		self.blast = self.head[-1]
		if len(self.head) < self.l:
			self.head.append([])
		self.f.f.addstr(self.head[0][0], self.head[0][1], ' ')
		j = [self.head[0][0], self.head[0][1]]

		if self.direction == "dUp":
			self.head.insert(0, [self.head[0][0] - 1, self.head[0][1]])
		if self.direction == "dDown":
			self.head.insert(0, [self.head[0][0] + 1, self.head[0][1]])
		if self.direction == "dLeft":
			self.head.insert(0, [self.head[0][0], self.head[0][1] - 1])
		if self.direction == "dRight":
			self.head.insert(0, [self.head[0][0], self.head[0][1] + 1])

		self.head.pop()

		if self.head[0] in self.head[1:]:
			kill()

	def setDirection(self, direction):
		self.direction = direction
	
	def printSnake(self):
		self.f.f.addstr(self.head[0][0], self.head[0][1], 'O', curses.COLOR_GREEN)

		i = 0
		for x in self.head[1:]:
			i += 1

			if x != []:
				try:
					self.f.f.addstr(self.head[i][0], self.head[i][1], '$')
				except:
					pass
			else:
				return

		try:
			if self.blast:
				self.f.f.addstr(self.blast[0], self.blast[1], ' ')
		except:
			pass

class Apple():
	def __init__(self, field):
		self.f = field
		self.Y, self.X = random.randrange(self.f.f.getmaxyx()[0]), random.randrange(self.f.f.getmaxyx()[1])
	
	def draw(self):
		self.f.f.addstr(self.Y, self.X, '@')

def kill():
	sys.exit()
	
def main(stdscr):
	dimX = 10
	dimY = 10
	length = 4
	hill = Field()
	snek = Snake(length, hill) 
	apple = Apple(hill)
	
	curses.curs_set(False)
	curses.start_color()
	
	stdscr.clear()
	stdscr.nodelay(1)

	snek.construct()

	while True:
		c = stdscr.getch()
		if c == ord('q'):
			break
		if c == ord('c'):
			stdscr.clear()
		elif c == curses.KEY_UP:
			snek.direction = 'dUp'
		elif c == curses.KEY_DOWN:
			snek.direction = 'dDown'
		elif c == curses.KEY_LEFT:
			snek.direction = 'dLeft'
		elif c == curses.KEY_RIGHT:
			snek.direction = 'dRight'

		hill.f.addstr(0,0, 'Length' + '\t' + str(snek.l))
		hill.f.addstr(1,0, str(snek.head))

		snek.move()
		if snek.head[0] == [apple.Y, apple.X]:
			del apple
			apple = Apple(hill)
			snek.l += 1

		snek.printSnake()
		apple.draw()

		hill.f.refresh()
		curses.napms(200)


wrapper(main)
