import pygame, pics_loading, visuals, math, copy

castlingLadyas = []
mat = False

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
		self.sx = 64
		self.sy = 64
		self.steps = 0
		self.steps_m = [[False for i in range(8)] for j in range(8)]
		self.areStepsCreated = False
		self.trans = 25
		self.figures_trans = 255
		self.isMoving = False
		self.an = 0
		self.vx = 0
		self.vy = 0
		self.ticker = 0
		self.figures = []
		self.allowedToMove = True
		self.defendingTheKing = False
		self.firstMove = True

	def move(self, event, desk, hod):
		global castlingLadyas, mat
		needToKill = False
		mat = False
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
											if castlingLadya.x > self.x:
												forced_move(castlingLadya, desk, j-1, self.y)
											else:
												forced_move(castlingLadya, desk, j+1, self.y)
											castlingEnded = True
							if desk[i][j]!=self.color and desk[i][j]!=-1: needToKill = True
							self.firstMove = False
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
							self.defendingTheKing = False
							castlingLadyas = []
							hod += 1
							for f in self.figures:
								if f.color!=self.color and type(f)==King:
									mat = defendTheKing(f, desk)
									break
							return hod, needToKill, mat
		
		self.areStepsCreated = False
		return hod, needToKill, mat

	def steps_draw(self, surf, desk):
		if not(self.areStepsCreated) and self.allowedToMove and not(self.defendingTheKing):
			self.steps_m = self.goes(desk)
			self.areStepsCreated = True
		if type(self)==King and not(self.areStepsCreated):
			self.steps_m = self.goes(desk)
			self.areStepsCreated = True
		if self.allowedToMove:
			visuals.trans(self)
			steps = self.steps_m
			self.areStepsCreated = True
			green = pics_loading.visuals_loading()[1]
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
		figures_temp = self.figures
		for i in range(len(steps)):
			for j in range(len(steps[i])):
				if steps[i][j]:
					desk_temp = copy.deepcopy(desk)
					desk_temp[i][j] = self.color
					desk_temp[self.y][self.x] = -1
					if len(attackingFigures)==1:
						for af in attackingFigures:
							if af.x == j and af.y == i:
								self.allowedToMove = True
								self.defendingTheKing = True
								self.steps_m[i][j] = True
								attackingFigures.remove(af)

					new_attacking_steps = self.howCanWeKillTheKing(desk_temp, figures_temp)

					if type(self)==King:
						king_x = j
						king_y = i
					if not(new_attacking_steps[king_y][king_x]): 
						self.allowedToMove = True
						self.defendingTheKing = True
						self.steps_m[i][j] = True

		if type(self)==King and self.steps_m == [[False for i in range(8)] for j in range(8)]:
			mat = True

class Pawn(Figure):
	def __init__(self,x,y, color):
		super().__init__(x,y, color)
		self.attackingSteps = []
	
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
		self.attackingSteps = [[False for i in range(8)] for j in range(8)]
		if self.color == 0: k = -1 #white
		else: k = 1 #black
		if not(self.y+2*k == 8 or self.y+2*k == -1 or self.y+2*k == -2 or self.y+2*k == 9):
			if self.steps == 0 and not(desk[self.y + 2*k][self.x]!=-1 or desk[self.y + k][self.x]!=-1): #двигаем пешку первым ходом
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