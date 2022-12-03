import pygame, math, steps, figures, pics_loading

pygame.init()

WIDTH = 1080
HEIGHT = 720

font = pygame.font.SysFont('Comic Sans', 40)


sc = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess'N'Guns")

FPS = 60
clock = pygame.time.Clock()

figurs = [figures.Pawn(x = 0, y = 1, color = 1), figures.Pawn(x = 1, y = 1, color = 1),
		  figures.Pawn(x = 0, y = 6, color = 0), figures.Pawn(x = 5, y = 6, color = 0),
		  figures.Pawn(x = 1, y = 5, color = 1),
		  figures.Ladya(x = 7, y = 0, color = 1), figures.Ladya(x = 0, y = 0, color = 1),
		  figures.Ladya(x = 7, y = 7, color = 0), figures.Ladya(x = 0, y = 7, color = 0),
		  figures.Bishop(x = 6, y = 0, color = 1), figures.Bishop(x = 1, y = 0, color = 1),
		  figures.Bishop(x = 6, y = 7, color = 0), figures.Bishop(x = 1, y = 7, color = 0),
		  figures.Horse(x = 5, y = 0, color = 1), figures.Horse(x = 2, y = 0, color = 1),
		  figures.Horse(x = 5, y = 7, color = 0), figures.Horse(x = 2, y = 7, color = 0),
		  figures.Queen(x = 4, y = 0, color = 1), figures.Queen(x = 3, y = 7, color = 0),
		  figures.King(x = 3, y = 0, color = 1), figures.King(x = 4, y = 7, color = 0)]

desk = [[-1 for i in range(8)] for j in range(8)]
finished = False
ticker = 0
hod = 0

def click(event):
	"""
	сумасшедшая функция, отвечающая за нажатие
	здесь производится нажатие на фигуру и проверка, если игрок делает верный ход нажатой фигуры
	"""
	global figurs, desk, hod
	x = event.pos[0]
	y = event.pos[1]
	r = False
	change_hod = hod
	for f in figurs:
		last_one = 0
		b = (f.color == 0 and hod%2==0) or (f.color == 1 and hod%2==1)
		
		if f.clicked and b: 
			hod = f.move(event, desk, hod)
			last_one = f
		if x < (f.x+1)*64+284 and x >= f.x*64+284 and y >= f.y*64+104 and y < (f.y+1)*64+104 and b and not(last_one):
			f.clicked = True
			r = True
		else:
			f.clicked = False
	if change_hod!=hod:
		for f in figurs:
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
		figura.draw(desk_sc, desk)

	if hod%2==0: shod= 'Ход белых'
	else: shod = 'Ход чёрных'
	hodt = font.render(shod, 1, (220,220,220))
	rg.blit(hodt, (100, 100))

	rg.blit(desk_sc, (284, 104))

	return rg

while not finished: #main cycle
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
