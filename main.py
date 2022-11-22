import pygame, math, steps, figures, pics_loading

pygame.init()

WIDTH = 1080
HEIGHT = 720

sc = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess'N'Guns")

FPS = 60
clock = pygame.time.Clock()

figurs = [figures.Pawn(x = 1, y = 0), figures.Pawn(x = 2, y = 5)]

desk = [[0 for i in range(8)] for j in range(8)]
print(desk)
finished = False
ticker = 0

def click(event):
	global figurs
	x = event.pos[0]
	y = event.pos[1]
	r = False
	for f in figurs:
		if x < (f.x+1)*64+284 and x >= f.x*64+284 and y >= f.y*64+104 and y < (f.y+1)*64+104:
			f.clicked = True
			r = True
		else:
			f.clicked = False
	if r: return True
	for f in figurs:
		f.clicked = False
	return False

def render():
	global desk_im
	rg = pygame.Surface((1080,720))

	rg.fill((50,50,50))

	desk_sc = pygame.Surface((512,512))
	desk_sc.blit(pics_loading.visuals_loading()[0], (0,0))

	for figura in figurs:
		figura.draw(desk_sc)

	rg.blit(desk_sc, (284, 104))

	return rg

while not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			click(event)
		if event.type == pygame.MOUSEBUTTONUP:
			pass

	clock.tick(FPS)
	sc.blit(render(), (0,0))
	pygame.display.update()
