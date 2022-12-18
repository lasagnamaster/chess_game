import pygame, math, steps, figures, pics_loading, Button, config, copy, random

import visuals

pygame.init()

WIDTH = 1080
HEIGHT = 720

font = pygame.font.SysFont('Times New Roman', 32)
font = pygame.font.Font('DungeonChunk.ttf', 32)

mainmenu_music_is_playing = 0
game_music_is_playing = 0
pause_music_is_playing = 0
volume = 0
UpVolume = False
sc = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess'N'Guns")

FPS = 60
clock = pygame.time.Clock()

buttons = [Button.Start(x = 390, y = 200, image = pics_loading.BUTTON_PICS[0], under_mouse_image= pics_loading.BUTTON_PICS[1]),
		   Button.Quit(x = 390, y = 350, image = pics_loading.BUTTON_PICS[2], under_mouse_image= pics_loading.BUTTON_PICS[3])]

buttons_pause = [Button.Resume(x = 390, y = 200, image = pics_loading.BUTTON_PICS[6], under_mouse_image= pics_loading.BUTTON_PICS[7]),
				 Button.Menu_Open(x = 390, y = 350, image = pics_loading.BUTTON_PICS[4], under_mouse_image= pics_loading.BUTTON_PICS[5])]

figurs = config.figurs_start_posssison


figurs1 = [figures.Ladya(x = 7, y = 7, color = 0), figures.Ladya(x = 0, y = 7, color = 0),
		  figures.Ladya(x = 7, y = 0, color = 1), figures.Ladya(x = 0, y = 0, color = 1),
		  figures.King(x = 3, y = 7, color = 0),
		  figures.King(x = 4, y = 0, color = 1)]

desk = [[-1 for i in range(8)] for j in range(8)]
finished = False
ticker = 0
hod = 0
mat = False

for f in figurs:
	f.FiguresImport(figurs)

def initNewGame():
	global desk, hod
	figurs_start_posssison = [figures.Pawn(x=0, y=6, color=0), figures.Pawn(x=1, y=6, color=0),
							  figures.Pawn(x=2, y=6, color=0), figures.Pawn(x=3, y=6, color=0),
							  figures.Pawn(x=4, y=6, color=0), figures.Pawn(x=5, y=6, color=0),
							  figures.Pawn(x=6, y=6, color=0), figures.Pawn(x=7, y=6, color=0),
							  figures.Pawn(x=0, y=1, color=1), figures.Pawn(x=1, y=1, color=1),
							  figures.Pawn(x=2, y=1, color=1), figures.Pawn(x=3, y=1, color=1),
							  figures.Pawn(x=4, y=1, color=1), figures.Pawn(x=5, y=1, color=1),
							  figures.Pawn(x=6, y=1, color=1), figures.Pawn(x=7, y=1, color=1),

							  figures.Ladya(x=7, y=7, color=0), figures.Ladya(x=0, y=7, color=0),
							  figures.Ladya(x=7, y=0, color=1), figures.Ladya(x=0, y=0, color=1),
							  figures.Horse(x=6, y=7, color=0), figures.Horse(x=1, y=7, color=0),
							  figures.Horse(x=6, y=0, color=1), figures.Horse(x=1, y=0, color=1),
							  figures.Bishop(x=5, y=7, color=0), figures.Bishop(x=2, y=7, color=0),
							  figures.Bishop(x=5, y=0, color=1), figures.Bishop(x=2, y=0, color=1),
							  figures.Queen(x=4, y=7, color=0), figures.Queen(x=3, y=0, color=1),
							  figures.King(x=3, y=7, color=0),
							  figures.King(x=4, y=0, color=1)]
	for f in figurs_start_posssison:
		f.firstMove = True
	desk = [[-1 for i in range(8)] for j in range(8)]
	hod = 0
	return figurs_start_posssison
def IsQuit():
	global finished
	if Button.Finish == True:
		finished = True
def search_n_kill(x,y,last_one):
	global figurs
	for f in figurs:
		if f.x == x and f.y == y and f!=last_one:
			figurs.remove(f)
		
def pawn_to_queen():
	global figurs
	for f in figurs:
		if type(f)==figures.Pawn and ((f.color == 0 and f.y == 0) or (f.color == 1 and f.y == 7)) and f.isMoving == False:
			figurs.append(figures.Queen(x = f.x, y = f.y, color = f.color))
			figurs.remove(f)

def click(event):
	"""
	сумасшедшая функция, отвечающая за нажатие
	здесь производится нажатие на фигуру и проверка, если игрок делает верный ход нажатой фигуры
	"""
	global figurs, desk, hod, ticker, started_ticker, mat
	x = event.pos[0]
	y = event.pos[1]
	r = False
	change_hod = hod
	for f in figurs:
		last_one = 0
		whatColorIsMoving = (f.color == 0 and hod%2==0) or (f.color == 1 and hod%2==1)
		
		if f.clicked and whatColorIsMoving: 
			result = f.move(event, desk, hod)
			
			hod = result[0]
			mat = result[2]
			last_one = f
			if result[1]:
				search_n_kill(f.x,f.y,last_one)

		if x < (f.x+1)*64+284 and x >= f.x*64+284 and y >= f.y*64+104 and y < (f.y+1)*64+104 and whatColorIsMoving and not(last_one):
			figures.defendTheKing(f,desk)
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

def UpVolumeFun():
	global volume
	if UpVolume == True:
		if volume <= 0.1:
			volume = 0.1
		else:
			volume -= 0.01
	else:
		if volume >= 1:
			volume = 1
		else:
			volume += 0.01
	pygame.mixer.music.set_volume(volume)
	if Button.Menu == False and Button.Pause_Menu == False:
		pygame.mixer.music.set_volume(volume)
def render():
	global desk_im, mat, mainmenu_music_is_playing, game_music_is_playing, pause_music_is_playing, volume, UpVolume
	if Button.Menu == True:
		pause_music_is_playing = 0
		game_music_is_playing = 0
		if not mainmenu_music_is_playing:
			pygame.mixer.music.load(pics_loading.MUSIC[random.randint(0,2)])
			pygame.mixer.music.play()
			mainmenu_music_is_playing = 1

		rg = pygame.Surface((1080,720))
		rg.blit(pics_loading.VISUALS_PICS[3], (0,0))
		for b in buttons:
			b.draw(rg)

	elif Button.Pause_Menu == True:
		mainmenu_music_is_playing = 0
		if not pause_music_is_playing:
			UpVolume = True
			pause_music_is_playing = 1

		rg = pygame.Surface((1080,720))
		rg.blit(pics_loading.VISUALS_PICS[5], (0,0))
		for b in buttons_pause:
			b.draw(rg)
	else:
		pause_music_is_playing = 0
		mainmenu_music_is_playing = 0
		if not game_music_is_playing:
			pygame.mixer.music.load(pics_loading.MUSIC[random.randint(3,6)])
			pygame.mixer.music.play()
			game_music_is_playing = 1

		else:
			#pygame.mixer.music.set_volume(volume)
			UpVolume = False
		rg = pygame.Surface((1080,720))

		rg.blit(pics_loading.VISUALS_PICS[4], (0,0))

		desk_sc = pygame.Surface((512,512)).convert_alpha()
		desk_sc.set_colorkey((0,0,0))
		desk_sc.set_alpha(255)
		desk_sc.blit(pics_loading.VISUALS_PICS[0], (0,0))

		shah = ''
		if hod%2==1: nameOfTheColor = 1
		else: nameOfTheColor = 0

		for figura in figurs:
			figura.draw(desk_sc, desk)
			if type(figura)==figures.King and figura.color==nameOfTheColor:
				if figura.underAttack and not(mat):
					shah = 'Шах'
				elif figura.underAttack and mat:
					shah = 'Мат'
				else: shah = ''

		pawn_to_queen()
		if hod%2==0: shod= 'BLACK NIGGER'
		else: shod = 'WHITE POWER'

		hodt = font.render(shod, 1, (220,220,220))
		shaht = font.render(shah, 1, (240,50,50))

		rg.blit(hodt, (100, 100))
		rg.blit(shaht, (100, 200))

		if mat:
			gameOverScreen()

		rg.blit(desk_sc, (284, 104))
	return rg

def gameOverScreen():
	pass
def Which_Button_Clicked():
	global figurs, hod
	if Button.Menu == True:
		for b in buttons:
			b.click()
			if Button.Is_New_Game == True:
				figurs = initNewGame()
				hod = 0
	elif Button.Pause_Menu == True:
		for b in buttons_pause:
			b.click()

while not finished: #main cycle
	ticker+=1
	IsQuit()
	UpVolumeFun()
	for f in figurs:
		f.FiguresImport(figurs)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				Button.Pause_Menu = not Button.Pause_Menu
				Button.Is_New_Game = False
		elif event.type == pygame.MOUSEMOTION:
			visuals.IsGunRotate()
		elif event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			click(event)
			Which_Button_Clicked()


		elif event.type == pygame.MOUSEBUTTONUP:
			for b in buttons_pause:
				b.clicked = False
			for b in buttons:
				b.clicked = False

	clock.tick(FPS)
	sc.blit(render(), (0,0))
	pygame.display.update()