import pygame, pics_loading

class Figure:
	"""
	initialize figure
	color 0 - white
	color 1 - black

	surf - desk
	self.surf - pics of figures
	"""
	def __init__(self,x = 0, y = 0, color = 0):
		self.x = x
		self.y = y
		self.color = color
		self.clicked = False
		self.transformed = False
		self.surf = pygame.Surface((64,64))
		self.sx = 64
		self.sy = 64
		self.steps = 0

	def draw(self, surf):
		pass

class Pawn(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)
	
	def draw(self, surf, desk):
		desk[self.y][self.x] = True
		if self.clicked:
			if not(self.transformed): #штука для красивого уменьшения фигурки
				self.sx-=3
				self.sy-=3
				if self.color == 1: self.surf = pygame.transform.scale(pics_loading.figures_loading()[0], (self.sx, self.sy))
				elif self.color == 0: self.surf = pygame.transform.scale(pics_loading.figures_loading()[1], (self.sx, self.sy))
				if self.sx<=50:
					self.transformed = True
			steps = self.goes(desk)
			green = pics_loading.visuals_loading()[1]
			for i in range(len(steps)):
				for j in range(len(steps[i])):
					if steps[i][j]:
						surf.blit(green, (j*64, i*64))
		else: 
			#если на фигуру не нажали, то мы рисуем её изначальный вид
			self.surf = pygame.Surface((64,64))
			if self.color == 1: self.surf.blit(pics_loading.figures_loading()[0],(0,0))
			else: self.surf.blit(pics_loading.figures_loading()[1],(0,0))
			self.sx = 64
			self.sy = 64
			self.transformed = False

		rect = self.surf.get_rect(center = (self.x*64+32, self.y*64+32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		steps = [[False for i in range(8)] for j in range(8)]
		if self.color == 0: k = -1 #white
		else: k = 1 #black
		if not(self.y+2*k == 8 or self.y+2*k == -1 or self.y+2*k == -2 or self.y+2*k == 9):
			if self.steps == 0 and not(desk[self.y + 2*k][self.x] or desk[self.y + k][self.x]): #moving pawn on its first move
				steps[self.y + 2*k][self.x]=True
			if self.y + k != 8 or self.y + k != -1:
				if not(desk[self.y + k][self.x]):
					steps[self.y + k][self.x]=True
		#need fix
		
		#if desk[self.y+k][self.x+1]:
			#steps[self.y+k][self.x+1] = True
		#if desk[self.y+k][self.x-1]:
			#steps[self.y+k][self.x-1] = True
		
		return steps

	def move(self, event, desk, hod):
		steps = self.goes(desk)
		x0 = event.pos[0]
		y0 = event.pos[1]
		if self.color == 0: k = -1 #white
		else: k = 1 #black
		for i in range(len(steps)):
			for j in range(len(steps[i])):
				if steps[i][j]:
					steps[i][j]==False
					if x0 < (j+1)*64+284 and x0 >= j*64+284 and y0 >= i*64+104 and y0 < (i+1)*64+104:
						self.y = i
						self.x = j
						self.steps+=1
						self.transformed = False
						self.clicked = False
						hod += 1
						print(hod)
						return hod
		return hod

class Ladya(Figure):
	pass

class Slon(Figure):
	pass

class Horse(Figure):
	pass

class Queen(Figure):
	pass

class King(Figure):
	pass

def desk_print(desk):
	for i in desk:
		print(i)