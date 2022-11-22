import pygame, pics_loading

class Figure:
	"""
	initialize figure
	color 0 - white
	color 1 - black
	"""
	def __init__(self,x = 0, y = 0):
		self.x = x
		self.y = y
		self.color = 0
		self.clicked = False
		self.transformed = False
		self.surf = pygame.Surface((64,64))
		self.sx = 64
		self.sy = 64

	def draw(self, surf):
		pass

class Pawn(Figure):
	def __init__(self,x,y):
		super().__init__(x,y)
	
	def draw(self, surf):
		if self.clicked:
			if not(self.transformed):
				self.sx-=3
				self.sy-=3
				self.surf = pygame.transform.scale(pics_loading.figures_loading()[0], (self.sx, self.sy))
				if self.sx<=50:
					self.transformed = True
		else: 
			self.surf = pygame.Surface((64,64))
			self.surf.blit(pics_loading.figures_loading()[0],(0,0))
			self.sx = 64
			self.sy = 64
			self.transformed = False

		rect = self.surf.get_rect(center = (self.x*64+32, self.y*64+32))
		surf.blit(self.surf, rect)

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
