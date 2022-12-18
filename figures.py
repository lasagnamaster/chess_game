import pygame, pics_loading, visuals, math, copy, random, shop

castlingLadyas = []
mat = False

def clear():
	file = open("memory.txt","w") #Очистка файла
	file.write('')
	file.close()

def fileWrite(info):
	file = open("memory.txt","a")
	for e in info:
		file.write(str(e)+' ')
	file.write('\n')
	file.close()

def fileRead():
	file = open("memory.txt","r")
	s = "balaboba"
	fullInfo = []
	while s:
		s = file.readline().strip().split()
		fullInfo.append(s)
	file.close()
	return fullInfo

class Figure:
	"""
	initialize figure
	color 0 - белый цвет
	color 1 - черный цвет
	self.x и self.y - положение фигуры на доске в координатах от 0 до 7
	self.x1 и self.y1 - положение фигуры на доске в обычных координатах
	self.transformed - уменьшили ли мы фигуру после нажатия
	self.steps_m - массив с разрешёнными ходами (нужно для отрисовывания зелёных клеток)
	self.surf - картинки фигур
	self.figures - массив фигур, загружаемый из мэйна
	self.allowedToMove - объясняет само себя, может ли фигура двигаться на этом ходе
	self.defendingTheKing - проверка, если фигура защищает короля от потенциального мата
	self.firstMove = True - сходила ли фигура на первом ходу
	
	"""
	def __init__(self,x = 0, y = 0, color = 0, figures_trans = 255):
		self.x = x
		self.y = y
		self.x1 = self.x*64
		self.y1 = self.y*64
		self.color = color
		self.clicked = False
		self.transformed = False
		self.surf = pygame.Surface((64,64))
		self.s = [64, 64]
		self.steps = 0
		self.steps_m = [[False for i in range(8)] for j in range(8)]
		self.areStepsCreated = False
		self.trans = 25
		self.figures_trans = 255
		self.isMoving = False
		self.vx = 0
		self.vy = 0
		self.ticker = 0
		self.figures = []
		self.allowedToMove = True
		self.defendingTheKing = False
		self.firstMove = True
		self.health = 100
		self.payment = 0
		self.gun_trans = 0

	def move(self, event, desk, hod):
		global castlingLadyas, mat
		needToKill = False
		mat = False
		wasCastling = 0
		if self.allowedToMove: 
			steps = self.goes(desk)
			if self.defendingTheKing: steps = self.steps_m
			x0 = event.pos[0]
			y0 = event.pos[1]
			for i in range(len(steps)):
				for j in range(len(steps[i])):
					if steps[i][j]:
						steps[i][j]==False
						if x0 < (j+1)*64+284 and x0 >= j*64+284 and y0 >= i*64+104 and y0 < (i+1)*64+104:

							rook_x = 0
							rook_y = 0
							rook_x1 = 0
							rook_y1 = 0

							if type(self)==King: #Рокировка
								if self.castlingMoves[i][j]:
									castlingEnded = False
									castlingLadya = 0
									for f in self.figures:
										if type(f)==Ladya and f.color==self.color and f in castlingLadyas and not(castlingEnded):
											if len(castlingLadyas)==2:
												if abs(x0 - (castlingLadyas[0].x*64+284)) < abs(x0 - (castlingLadyas[1].x*64+284)): castlingLadya = castlingLadyas[0]
												else: castlingLadya = castlingLadyas[1]
											else: castlingLadya = castlingLadyas[0]
											rook_x = castlingLadya.x
											rook_y = castlingLadya.y
											if castlingLadya.x > self.x:
												forced_move(castlingLadya, desk, j-1, self.y)
												rook_x1 = j-1
												rook_y1 = self.y
											else:
												forced_move(castlingLadya, desk, j+1, self.y)
												rook_x1 = j+1
												rook_y1 = self.y
											castlingEnded = True
											wasCastling = 1

							fileWrite([wasCastling, self.x, self.y, j, i, rook_x, rook_y, rook_x1, rook_y1])
							if desk[i][j]!=self.color and desk[i][j]!=-1: needToKill = True
							self.firstMove = False
							self.x0 = j*64
							self.y0 = i*64
							desk[self.y][self.x] = -1
							self.x = j
							self.y = i
							desk[i][j] = self.color
							visuals.AnimationUgol(self)
							self.isMoving = True
							self.steps+=1
							self.transformed = False
							self.clicked = False
							self.areStepsCreated = False
							self.defendingTheKing = False
							castlingLadyas = []
							pics_loading.SOUNDS[random.randint(0, 5)].play()
							hod += 1
							for f in self.figures:
								if f.color!=self.color and type(f)==King:
									mat = defendTheKing(f, desk)
									break
							
							self.steps_m = [[False for i in range(8)] for j in range(8)]
							return hod, needToKill, mat
		self.steps_m = [[False for i in range(8)] for j in range(8)]
		self.areStepsCreated = False
		return hod, needToKill, mat

	def steps_draw(self, surf, desk):
		if not(self.areStepsCreated) and self.allowedToMove and not(self.defendingTheKing):
			self.steps_m = self.goes(desk)
			self.areStepsCreated = True
		if type(self)==King and not(self.areStepsCreated):
			self.steps_m = self.goes(desk)
			self.areStepsCreated = True
			defendTheKing(self,desk)
		if self.allowedToMove:
			visuals.trans(self)
			steps = self.steps_m
			self.areStepsCreated = True
			green = pics_loading.VISUALS_PICS[1]
			green.set_alpha(self.trans)
			for i in range(len(steps)):
				for j in range(len(steps[i])):
					if steps[i][j]:
						surf.blit(green, (j*64, i*64))

	def FiguresImport(self, Figures):
		self.figures = Figures

	def howCanWeKillTheKing(self, desk, figures):
		attacking_steps = [[False for i in range(8)] for j in range(8)]
		for f in figures:
			if f.color!=self.color and type(f)!=Pawn and type(f)!=King:
				steps_temp = f.goes(desk)
			elif f.color!=self.color and (type(f)==Pawn or type(f)==King):
				f.goes(desk)
				steps_temp = f.attackingSteps
			if f.color!=self.color:
				for i in range(len(steps_temp)):
					for j in range(len(steps_temp[i])):
						if steps_temp[i][j]: attacking_steps[i][j] = True
		return attacking_steps

	def ghostSteps(self, desk, king_x, king_y, attackingFigures):
		global mat
		attacking_steps = self.howCanWeKillTheKing(desk, self.figures)
		self.allowedToMove = False
		self.defendingTheKing = False
		self.steps_m = [[False for i in range(8)] for j in range(8)]
		steps = self.goes(desk)
		for i in range(len(steps)): #тут происходят призрачные шаги, проверка, что будет с королём при различных ходах фигуры
			for j in range(len(steps[i])):
				if steps[i][j]:

					figures_temp = self.figures
					desk_temp = copy.deepcopy(desk)
					returnTheseBack = []

					desk_temp[i][j] = self.color
					desk_temp[self.y][self.x] = -1

					for f in figures_temp:
						if f.x==j and f.y==i and self.color!=f.color:
							print(type(f), i, j)
							figures_temp.remove(f)
							returnTheseBack.append(f)

					new_attacking_steps = self.howCanWeKillTheKing(desk_temp, figures_temp)
					
					if type(self)==King:
						king_x = j
						king_y = i
					if not(new_attacking_steps[king_y][king_x]): 
						self.allowedToMove = True
						self.defendingTheKing = True
						self.steps_m[i][j] = True
					for f in returnTheseBack:
						figures_temp.append(f)

		canSomeoneGo = False
		for f in self.figures:
			if f.color == self.color:
				print(type(f), f.color)
				desk_print(f.steps_m)
			if f.color==self.color and f.steps_m != [[False for i in range(8)] for j in range(8)]:
				canSomeoneGo = True
		if type(self)==King and self.steps_m == [[False for i in range(8)] for j in range(8)] and not(canSomeoneGo):
			mat = True

class Pawn(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)
		self.attackingSteps = []
		self.payment = 10
	
	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		gun_surf = pygame.Surface((0,0)).convert_alpha()
		if self.clicked:
			self.steps_draw(surf, desk)
			gun_surf = visuals.gun_move_and_rotate(self, pics_loading.VISUALS_PICS[2])
		else:
			self.gun_trans = 0

		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[0], pics_loading.FIGURES_PICS[1], surf, desk)
		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		rect1 = self.surf.get_rect(center = (self.x1-70, self.y1-65))
		surf.blit(gun_surf, rect1)
		surf.blit(self.surf, rect)

	def goes(self, desk):
		steps = [[False for i in range(8)] for j in range(8)]
		self.attackingSteps = [[False for i in range(8)] for j in range(8)]
		if self.color == 0: k = -1 #white
		else: k = 1 #black
		if not(self.y+2*k == 8 or self.y+2*k == -1 or self.y+2*k == -2 or self.y+2*k == 9):
			if self.firstMove and not(desk[self.y + 2*k][self.x]!=-1 or desk[self.y + k][self.x]!=-1): #двигаем пешку первым ходом
				steps[self.y + 2*k][self.x]=True
		if not(self.y + k == 8 or self.y + k == -1):
			if not(desk[self.y + k][self.x]!=-1):
				steps[self.y + k][self.x]=True

		if not(self.y+k == 8 or self.y+k == -1) and not(self.x == 7):
			self.attackingSteps[self.y+k][self.x+1] = True
			if desk[self.y+k][self.x+1]!=self.color and (desk[self.y+k][self.x+1]!=-1):
				steps[self.y+k][self.x+1] = True
		if not(self.y+k == 8 or self.y+k == -1) and not(self.x == 0):
			self.attackingSteps[self.y+k][self.x-1] = True
			if desk[self.y+k][self.x-1]!=self.color and (desk[self.y+k][self.x-1]!=-1):
				steps[self.y+k][self.x-1] = True

		return steps

class Ladya(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)
		self.payment = 20

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[2], pics_loading.FIGURES_PICS[3], surf, desk)

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
		self.payment = 15

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[4], pics_loading.FIGURES_PICS[5], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
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
		self.payment = 15

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[6], pics_loading.FIGURES_PICS[7], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
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
		self.payment = 40

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[8], pics_loading.FIGURES_PICS[9], surf, desk)

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
		self.underAttack = False
		self.attackingFigures = []
		self.castlingMoves = [] 
		self.attackingSteps = self.attackingStepsFunc()
		self.mat = False
		self.payment = 99999

	def draw(self, surf, desk):
		desk[self.y][self.x] = self.color
		if self.clicked:
			self.steps_draw(surf, desk)
		if self.isMoving == True:
			visuals.move_animation(self)
		visuals.scale_down(self, pics_loading.FIGURES_PICS[10], pics_loading.FIGURES_PICS[11], surf, desk)

		rect = self.surf.get_rect(center = (self.x1 +32, self.y1+ 32))
		surf.blit(self.surf, rect)

	def goes(self, desk):
		global castlingLadya
		steps = [[False for i in range(8)] for j in range(8)]
		
		for i in range(4):
			for k in range(1,2):
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
			for k in range(1,2):
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

		
		self.castlingMoves = [[False for i in range(8)] for j in range(8)] #Рокировка
		if self.firstMove and not(self.underAttack) and self.clicked:
			for f in self.figures:
				if f.color == self.color and type(f)==Ladya and f.firstMove:
					denyCastling = False
					if self.x > f.x:
						for i in range(f.x+1, self.x):
							if desk[self.y][i] != -1: denyCastling = True
							castlingKoef = -1
					else:
						for i in range(self.x+1, f.x):
							if desk[self.y][i] != -1: denyCastling = True
							castlingKoef = 1
					
					if not(denyCastling):
						if not(f in castlingLadyas):
							if len(castlingLadyas)!=0:
								if f.color==castlingLadyas[0].color:
									castlingLadyas.append(f)
							else:
								castlingLadyas.append(f)

						steps[self.y][self.x+2*castlingKoef] = True
						self.castlingMoves[self.y][self.x+2*castlingKoef] = True
			
		self.underAttack = False
		self.attackingFigures = []
		self.attackingStepsFunc()
		for f in self.figures: #Чтобы нельзя было ходить королём в места, где можно поставить шах
			if type(f)!=King and type(f)!=Pawn and f.color!=self.color:
				enemies_steps = f.goes(desk)
				for i in range(len(steps)):
					for j in range(len(steps[i])):
						if steps[i][j] and enemies_steps[i][j]:
							steps[i][j] = False
						if enemies_steps[i][j] and i==self.y and j==self.x:
							self.underAttack = True
							if f not in self.attackingFigures:
								self.attackingFigures.append(f)
								
			elif type(f) == Pawn and f.color!=self.color:
				f.goes(desk)
				for i in range(len(f.attackingSteps)):
					for j in range(len(steps[i])):
						if steps[i][j] and f.attackingSteps[i][j]:
							steps[i][j] = False
						if f.attackingSteps[i][j] and i==self.y and j==self.x:
							self.underAttack = True
							if f not in self.attackingFigures:
								self.attackingFigures.append(f)
			
			elif type(f) == King and f.color!=self.color:
				f.attackingStepsFunc()
				for i in range(len(steps)):
					for j in range(len(steps[i])):
						if f.attackingSteps[i][j] and steps[i][j]:
							steps[i][j] = False
		return steps

	def attackingStepsFunc(self):
		k = 1
		self.attackingSteps = [[False for i in range(8)] for j in range(8)]
		if border_check(self.y, k):
			self.attackingSteps[self.y+k][self.x]=True
		if border_check(self.y, -k):
			self.attackingSteps[self.y-k][self.x]=True
		if border_check(self.x, k):
			self.attackingSteps[self.y][self.x+k]=True
		if border_check(self.x, -k):
			self.attackingSteps[self.y][self.x-k]=True
		if border_check(self.y, k) and border_check(self.x, k):
			self.attackingSteps[self.y+k][self.x+k]=True
		if border_check(self.y, -k) and border_check(self.x, k):
			self.attackingSteps[self.y-k][self.x+k]=True
		if border_check(self.y, k) and border_check(self.y, -k):
			self.attackingSteps[self.y+k][self.x-k]=True
		if border_check(self.y, -k) and border_check(self.x, -k):
			self.attackingSteps[self.y-k][self.x-k]=True

def desk_print(desk):
	for i in desk:
		print(i)
	print('\n')

def border_check(coord, koef):
	if koef>0 and coord+koef<=7: return True
	if koef<0 and coord+koef>=0: return True
	return False

def defendTheKing(obj, desk):
	global mat
	areWeKillingTheKing = False
	for f in obj.figures:
		if f.color==obj.color and type(f)==King:
			f.goes(desk)
			king_x = f.x
			king_y = f.y
			attackingFigures = f.attackingFigures
			if f.underAttack: 
				areWeKillingTheKing = True
	if areWeKillingTheKing:
		obj.ghostSteps(desk, king_x, king_y, attackingFigures)
		obj.areStepsCreated = True

	else:
		for f in obj.figures:
			f.allowedToMove = True
			f.defendingTheKing = False
		obj.ghostSteps(desk, king_x, king_y, attackingFigures)
		if type(obj)!=King: #фикс для рокировки
			obj.areStepsCreated = True
	return mat

def forced_move(obj, desk, j, i):
	obj.firstMove = False
	obj.x0 = j*64
	obj.y0 = i*64
	desk[obj.y][obj.x] = -1
	obj.x = j
	obj.y = i
	visuals.AnimationUgol(obj)
	obj.isMoving = True

ticker = 0
i = 0
def rewind(desk, figures):
	global ticker, i
	ticker+=1
	fullInfo = fileRead()
	s = []
	if i < len(fullInfo):
		if ticker%25 == 0:
			s = fullInfo[i]
			i+=1
		if s:
			forced_move_rewind(int(s[0]), int(s[1]), int(s[2]), int(s[3]), int(s[4]), int(s[5]), int(s[6]), int(s[7]), int(s[8]), figures, desk)

def forced_move_rewind(wasCastling, x, y, x1, y1, x2, y2, x3, y3, figures, desk):
	global ticker
	print(x, y, x1, y1)
	
	for f in figures:
		if f.x==x1 and f.y==y1: 
			figures.remove(f)
			pics_loading.SOUNDS[random.randint(6, 11)].play()
		
		if f.x==x and f.y==y and wasCastling == 0:
			color = f.color
			pics_loading.SOUNDS[random.randint(0, 5)].play()
			
			forced_move(f, desk, x1, y1)
			
		elif f.x==x and f.y==y and wasCastling == 1:
			pics_loading.SOUNDS[random.randint(0, 5)].play()
			forced_move(f, desk, x1, y1)
			for f in figures:
				if f.x == x2 and f.y == y2:
					forced_move(f, desk, x3, y3)

if __name__ == "__main__":
    print('you were not supposed to use this as main')