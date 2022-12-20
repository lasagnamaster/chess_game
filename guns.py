import pygame, visuals, pics_loading, math, figures, random

ticker = 1
amount = 0

class Gun:
	def __init__(self, x, y):
		self.x = x*64 + 32
		self.y = y*64 + 32
		self.surf = pygame.Surface((256,256))
		self.an = 0 #угол пушки
		self.an1 = 0 #уголь пульки
		self.pic = 0
		self.gun_trans = 255
		self.xb = [] #координаты пульки
		self.yb = []
		self.lb = 0 #длина пульки
		self.vb = 0
		self.shooting = False
		self.target = None

	def shoot(self, obj, hod):
		global amount
		pos = pygame.mouse.get_pos()
		for f in obj.figures:
			if f.color!=obj.color and f.color!=-1 and obj.shoot_m[f.y][f.x] and (pos[0]<(f.x+1)*64+284 and pos[0]>=f.x*64+284) and (pos[1]<(f.y+1)*64+104 and pos[1]>=f.y*64+104):
				self.shooting = True
				if type(obj) == figures.King:
					pics_loading.SOUNDS[12].play()
				else:
					pics_loading.SOUNDS[random.randint(14,16)].play()
				if type(obj)==figures.Pawn:
					obj.firstMove = False
				self.target = f
				self.xb.append(self.x)
				self.yb.append(self.y)
				ticker = 1
				amount = 1
				hod+=1
		return hod

	def draw(self):
		self.surf.fill((0,0,0))
		self.surf.set_colorkey((0,0,0))
		visuals.gun_move_and_rotate(self, self.pic)
		return self.surf

	def bullet_draw(self, surf, f, figurs, desk, coins):
		global ticker, amount
		an = self.an1
		endhere = False
		for i in range(len(self.xb)):

			self.xb[i]+=self.vb*math.cos(an)
			self.yb[i]+=self.vb*math.sin(an)
			pygame.draw.line(surf, (220, 40, 40), [self.xb[i],self.yb[i]], [self.xb[i] + self.lb*math.cos(an), self.yb[i] + self.lb*math.sin(an)], 3)
			x = self.xb[i]+self.lb//2*math.cos(an)
			y = self.yb[i]+self.lb//2*math.sin(an)
			if x >= self.target.x*64 and x < (self.target.x+1)*64 and y >= self.target.y*64 and y < (self.target.y+1)*64:
				self.xb.remove(self.xb[i])
				self.yb.remove(self.yb[i])
				self.target.health-=self.damage
				break
			elif x >= self.target.x*64+16 and x < (self.target.x+1)*64+16 and y >= self.target.y*64+16 and y < (self.target.y+1)*64+16 and self.shooting:
				self.xb.remove(self.xb[i])
				self.yb.remove(self.yb[i])
				self.target.health-=self.damage
				break
			if amount == self.bullets:
				endhere = True
				amount = 0

		if self.target.health <= 0:
			desk[self.target.y][self.target.x] = -1
			if self.target.color == 0: coins[1]+=self.target.payment
			else: coins[0]+=self.target.payment
			figurs.remove(self.target)

		if len(self.xb)==0:
			self.shooting = False
			self.xb = []
			self.yb = []
			
		ticker+=1

class Bazooka(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[0]
		self.vb = 25
		self.lb = 25
		self.damage = 10
		self.bullets = 1

class Arisaka(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[1]
		self.vb = 35
		self.lb = 25
		self.damage = 15
		self.bullets = 1

class PPSh(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[2]
		self.vb = 25
		self.lb = 25
		self.damage = 15
		self.bullets = 1

class Mosin(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[3]
		self.vb = 30
		self.lb = 34
		self.damage = 20
		self.bullets = 1

class DP_28(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[4]
		self.vb = 30
		self.lb = 25
		self.damage = 25
		self.bullets = 1

class Bar(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[5]
		self.vb = 25
		self.lb = 25
		self.damage = 5
		self.bullets = 1

class Pistol(Gun):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.pic = pics_loading.GUN_PICS[6]
		self.vb = 20
		self.lb = 25
		self.damage = 10
		self.bullets = 1

	
