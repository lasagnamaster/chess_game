import pygame, math

pygame.init()

FPS = 60
clock = pygame.time.Clock()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	clock.tick(FPS)

	pygame.display.update()
