import curses
from curses import wrapper
import os 
import time

"""
Snake head is working, can't get body to spawn or follow, get to run
"""
	
class Field():
	def __init__(self, dimX, dimY):
		self.X = dimX
		self.Y = dimY
		self.f = None

	def construct_field(self):
		pad = curses.newwin(0,0 )
		self.f = pad
		self.f.keypad(True)
		self.f.addstr(5, 5, "frik")
		"""
		for y in range(0,99):
			for x in range(0,99):
				pad.addch('.')
				
				# Displays a section of the pad in the middle of the screen.
				# (0,0) : coordinate of upper-left corner of pad area to display.
				# (5,5) : coordinate of upper-left corner of window area to be filled
				#         with pad content.
				# (20, 75) : coordinate of lower-right corner of window area to be
				#          : filled with pad content.
				self.f = pad
				pad.refresh( 0,0, 5,5, 20,75)
		"""

class GameField(Field):
	def __init__(self, field, worm):
		self.f = field
		self.worm = worm

	def construct(self):
		pass

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

	def check(self, coord):
		wcheck_s = str(self.head) + ' ' + str(coord) + '\n'
		with open('test.txt', 'w') as fi:
			fi.write(wcheck_s)
		if coord == self.head:
			return 1
		
	def move(self):
		z = 0
		j = []
		first = True

		self.blast = self.head[-1]
		if len(self.head) < self.l:
			self.head.append([])
		self.f.f.addstr(self.head[0][0], self.head[0][1], ' ')
		j = [self.head[0][0], self.head[0][1]]

		for x in self.head:
			curses.napms(500)
			self.f.f.addstr(2,0, str(z))
			self.f.f.addstr(3,0, str(j))
			if first:
				if self.direction == "dUp":
					self.head[0][0] = int(self.head[0][0] - 1)
				if self.direction == "dDown":
					self.head[0][0] = self.head[0][0] + 1
				if self.direction == "dLeft":
					self.head[0][1] = self.head[0][1] - 1
				if self.direction == "dRight":
					self.head[0][1] = self.head[0][1] + 1
				first = False
			
			elif x != []:
				self.head[i].pop()
				self.head.insert(z, self.head[z-1])
				self.f.f.addstr(6,0, str(self.head[z-1]))
				self.f.f.addstr(4,0, str(x))
			elif x == []:
				try:
					self.head[i].pop()
					self.head.insert(z, self.head[z-1])
					self.f.f.addstr(6,0, str(self.head[z-1]))
					self.f.f.addstr(4,0, str(x))
					return
				except:
					pass
			z += 1
				
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

def kill():
	pass
	
def gameLoop(gF):
	pass

def main(stdscr):
	dimX = 10
	dimY = 10
	length = 4
	hill = Field(dimX, dimY)
	snek = Snake(length, hill) 
	gF = GameField(hill, snek)
	
	curses.curs_set(False)
	curses.start_color()
	
	stdscr.clear()
	stdscr.nodelay(1)

	hill.construct_field()
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
		snek.printSnake()
		
		hill.f.refresh()
		curses.napms(200)


wrapper(main)
