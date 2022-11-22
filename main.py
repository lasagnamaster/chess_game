import pygame, math

pygame.init()

WIDTH = 1080
HEIGHT = 720

sc = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess'N'Guns")

FPS = 60
clock = pygame.time.Clock()

class Figure:
	"""
	initialize figure
	color 0 - white
	color 1 - black
	"""
	def __init__(x = 0, y = 0):
		self.x = x
		self.y = y
		self.color = 0
		self.type = 0

class Pawn(Figure):
	def __init__():
		pass

class Ladya(Figure):
	def __init__():
		pass

class Slon(Figure):
	def __init__():
		pass

class Horse(Figure):
	def __init__():
		pass

class Queen(Figure):
	def __init__():
		pass

class King(Figure):
	def __init__():
		pass

figures_position = []
desk = []
finished = False

while not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	clock.tick(FPS)

	#sc.blit(rendered_game, (0,0))
	pygame.display.update()
