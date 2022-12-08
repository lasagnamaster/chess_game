import pygame, pics_loading, visuals, math

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
		self.x1 = self.x*64
		self.y1 = self.y*64
		self.color = color
		self.clicked = False
		self.transformed = False
		self.surf = pygame.Surface((64,64))
		self.sx = 64
		self.sy = 64
		self.steps = 0
		self.steps_m = ''
		self.areStepsCreated = False
		self.trans = 25
		self.figures_trans = 255
		self.isMoving = False
		self.an = 0
		self.vx = 0
		self.vy = 0
		self.ticker = 0
		self.justEndedMoving = False

	def move(self, event, desk, hod):
		steps = self.goes(desk)
		
		x0 = event.pos[0]
		y0 = event.pos[1]

		print(self.an*180/3.1415)
		for i in range(len(steps)):
			for j in range(len(steps[i])):
				if steps[i][j]:
					steps[i][j]==False
					if x0 < (j+1)*64+284 and x0 >= j*64+284 and y0 >= i*64+104 and y0 < (i+1)*64+104:
	
						
						self.x0 = j*64
						self.y0 = i*64
						desk[self.y][self.x] = -1
						self.x = j
						self.y = i
						visuals.AnimationUgol(self)
						self.isMoving = True
						self.steps+=1
						self.transformed = False
						self.clicked = False
						self.areStepsCreated = False
						hod += 1

						return hod
		self.areStepsCreated = False
		return hod

	def steps_draw(self, surf, desk):
		
		if not(self.areStepsCreated):
			self.steps_m = self.goes(desk)
			self.areStepsCreated = True
		visuals.trans(self)
		steps = self.steps_m
		green = pics_loading.visuals_loading()[1]
		green.set_alpha(self.trans)
		for i in range(len(steps)):
			for j in range(len(steps[i])):
				if steps[i][j]:
					surf.blit(green, (j*64, i*64))


class Pawn(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)
	
	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[0], pics_loading.figures_loading()[1], surf, desk)
		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		steps = [[False for i in range(8)] for j in range(8)]
		if self.color == 0: k = -1 #white
		else: k = 1 #black
		if not(self.y+2*k == 8 or self.y+2*k == -1 or self.y+2*k == -2 or self.y+2*k == 9):
			if self.steps == 0 and not(desk[self.y + 2*k][self.x]!=-1 or desk[self.y + k][self.x]!=-1): #moving pawn on its first move
				steps[self.y + 2*k][self.x]=True
		if not(self.y + k == 8 or self.y + k == -1):
			if not(desk[self.y + k][self.x]!=-1):
				steps[self.y + k][self.x]=True

		if not(self.y+k == 8 or self.y+k == -1) and not(self.x == 7):
			if desk[self.y+k][self.x+1]!=self.color and (desk[self.y+k][self.x+1]!=-1):
				steps[self.y+k][self.x+1] = True
		if not(self.y+k == 8 or self.y+k == -1) and not(self.x == 0):
			if desk[self.y+k][self.x-1]!=self.color and (desk[self.y+k][self.x-1]!=-1):
				steps[self.y+k][self.x-1] = True
		
		return steps

class Ladya(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[2], pics_loading.figures_loading()[3], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		steps = [[False for i in range(8)] for j in range(8)]
		
		for i in range(4):
			for k in range(1,8):
				if border_check(self.y, k):
					if i==0 and desk[self.y + k][self.x]!=self.color: 
						steps[self.y+k][self.x]=True
						if desk[self.y + k][self.x]!=-1: break
					elif i == 0 and desk[self.y + k][self.x]==self.color: break
				if border_check(self.y, -k):
					if i==1 and desk[self.y - k][self.x]!=self.color: 
						steps[self.y-k][self.x]=True
						if desk[self.y-k][self.x]!=-1: break
					elif i == 1 and desk[self.y-k][self.x]==self.color: break
				if border_check(self.x, k):
					if i==2 and desk[self.y][self.x+k]!=self.color: 
						steps[self.y][self.x+k]=True
						if desk[self.y][self.x+k]!=-1: break
					elif i == 2 and desk[self.y][self.x+k]==self.color: break
				if border_check(self.x, -k):
					if i==3 and desk[self.y][self.x-k]!=self.color: 
						steps[self.y][self.x-k]=True
						if desk[self.y][self.x-k]!=-1: break
					elif i == 3 and desk[self.y][self.x-k]==self.color: break
		return steps

class Bishop(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[4], pics_loading.figures_loading()[5], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		#desk_print(desk)
		steps = [[False for i in range(8)] for j in range(8)]
		for i in range(4):
			for k in range(1,8):
				if border_check(self.y,k) and border_check(self.x, k):
					if i == 0 and desk[self.y + k][self.x+k]!=self.color: 
						steps[self.y+k][self.x+k]=True
						if desk[self.y + k][self.x + k]!=-1: break
					elif i == 0 and desk[self.y + k][self.x + k]==self.color: break
				if border_check(self.y,-k) and border_check(self.x, k):
					if i == 1 and desk[self.y - k][self.x+k]!=self.color: 
						steps[self.y-k][self.x+k]=True
						if desk[self.y - k][self.x + k]!=-1: break
					elif i == 1 and desk[self.y - k][self.x + k]==self.color: break
				if border_check(self.y,k) and border_check(self.x, -k):
					if i == 2 and desk[self.y + k][self.x - k]!=self.color: 
						steps[self.y+k][self.x-k]=True
						if desk[self.y + k][self.x - k]!=-1: break
					elif i == 2 and desk[self.y + k][self.x - k]==self.color: break
				if border_check(self.y,-k) and border_check(self.x, -k):
					if i == 3 and desk[self.y - k][self.x - k]!=self.color: 
						steps[self.y-k][self.x-k]=True
						if desk[self.y - k][self.x - k]!=-1: break
					elif i == 3 and desk[self.y - k][self.x - k]==self.color: break
		
		return steps

class Horse(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[6], pics_loading.figures_loading()[7], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		#desk_print(desk)
		steps = [[False for i in range(8)] for j in range(8)]
		if self.y<=5 and self.x<=6:
			if desk[self.y+2][self.x+1]!=self.color: steps[self.y+2][self.x+1]=True
		if self.y<=5 and self.x>=1:
			if desk[self.y+2][self.x-1]!=self.color: steps[self.y+2][self.x-1]=True
		if self.y>=2 and self.x<=6:
			if desk[self.y-2][self.x+1]!=self.color: steps[self.y-2][self.x+1]=True
		if self.y>=2 and self.x>=1:
			if desk[self.y-2][self.x-1]!=self.color: steps[self.y-2][self.x-1]=True

		if self.y<=6 and self.x<=5:
			if desk[self.y+1][self.x+2]!=self.color: steps[self.y+1][self.x+2]=True
		if self.y<=6 and self.x>=2:
			if desk[self.y+1][self.x-2]!=self.color: steps[self.y+1][self.x-2]=True
		if self.y>=1 and self.x<=5:
			if desk[self.y-1][self.x+2]!=self.color: steps[self.y-1][self.x+2]=True
		if self.y>=1 and self.x>=2:
			if desk[self.y-1][self.x-2]!=self.color: steps[self.y-1][self.x-2]=True
		
		return steps

class Queen(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[8], pics_loading.figures_loading()[9], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		#desk_print(desk)
		steps = [[False for i in range(8)] for j in range(8)]
		for i in range(4):
			for k in range(1,8):
				if border_check(self.y, k):
					if i==0 and desk[self.y + k][self.x]!=self.color: 
						steps[self.y+k][self.x]=True
						if desk[self.y + k][self.x]!=-1: break
					elif i == 0 and desk[self.y + k][self.x]==self.color: break
				if border_check(self.y, -k):
					if i==1 and desk[self.y - k][self.x]!=self.color: 
						steps[self.y-k][self.x]=True
						if desk[self.y-k][self.x]!=-1: break
					elif i == 1 and desk[self.y-k][self.x]==self.color: break
				if border_check(self.x, k):
					if i==2 and desk[self.y][self.x+k]!=self.color: 
						steps[self.y][self.x+k]=True
						if desk[self.y][self.x+k]!=-1: break
					elif i == 2 and desk[self.y][self.x+k]==self.color: break
				if border_check(self.x, -k):
					if i==3 and desk[self.y][self.x-k]!=self.color: 
						steps[self.y][self.x-k]=True
						if desk[self.y][self.x-k]!=-1: break
					elif i == 3 and desk[self.y][self.x-k]==self.color: break
		for i in range(4):
			for k in range(1,8):
				if border_check(self.y,k) and border_check(self.x, k):
					if i == 0 and desk[self.y + k][self.x+k]!=self.color: 
						steps[self.y+k][self.x+k]=True
						if desk[self.y + k][self.x + k]!=-1: break
					elif i == 0 and desk[self.y + k][self.x + k]==self.color: break
				if border_check(self.y,-k) and border_check(self.x, k):
					if i == 1 and desk[self.y - k][self.x+k]!=self.color: 
						steps[self.y-k][self.x+k]=True
						if desk[self.y - k][self.x + k]!=-1: break
					elif i == 1 and desk[self.y - k][self.x + k]==self.color: break
				if border_check(self.y,k) and border_check(self.x, -k):
					if i == 2 and desk[self.y + k][self.x - k]!=self.color: 
						steps[self.y+k][self.x-k]=True
						if desk[self.y + k][self.x - k]!=-1: break
					elif i == 2 and desk[self.y + k][self.x - k]==self.color: break
				if border_check(self.y,-k) and border_check(self.x, -k):
					if i == 3 and desk[self.y - k][self.x - k]!=self.color: 
						steps[self.y-k][self.x-k]=True
						if desk[self.y - k][self.x - k]!=-1: break
					elif i == 3 and desk[self.y - k][self.x - k]==self.color: break
		
		return steps

class King(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.figures_loading()[10], pics_loading.figures_loading()[11], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		steps = [[False for i in range(8)] for j in range(8)]
		
		
		return steps

def desk_print(desk):
	for i in desk:
		print(i)
	print('\n')

def border_check(coord, koef):
	if koef>0 and coord+koef<=7: return True
	if koef<0 and coord+koef>=0: return True
	return False