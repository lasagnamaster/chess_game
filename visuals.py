import pygame, figures, math

ColorSpeed = 4

def scale_down(obj, pic1, pic2, surf, desk):
	if obj.clicked:
		if not(obj.transformed):
			obj.sx-=4
			obj.sy-=4
			if obj.color == 1: obj.surf = pygame.transform.scale(pic1, (obj.sx, obj.sy))
			elif obj.color == 0: obj.surf = pygame.transform.scale(pic2, (obj.sx, obj.sy))
			if obj.sx<=50:
				obj.transformed = True
	else: 
		obj.surf = pygame.Surface((64,64)).convert_alpha()
		obj.surf.set_colorkey((0,0,0))
		if obj.color == 1:
			pic1.set_alpha(obj.figures_trans)
			obj.surf.blit(pic1,(0,0))
		else:
			pic2.set_alpha(obj.figures_trans)
			obj.surf.blit(pic2,(0,0))
		obj.sx = 64
		obj.sy = 64
		obj.transformed = False 

def trans(obj):
	global ColorSpeed
	if obj.areStepsCreated == True:
		if obj.trans + ColorSpeed >= 100:
			ColorSpeed = -4
		if obj.trans + ColorSpeed <= 20:
			ColorSpeed = +4
		obj.trans = obj.trans + ColorSpeed

def move_animation(obj):
	#не смотреть, не физики не поймут
	obj.ticker += 0.01
	obj.vx = (math.sqrt((obj.x1 - obj.x0)**2 + (obj.y0 - obj.y1)**2)*(2**0.5))*math.sin(obj.ticker)* math.cos(obj.an)
	obj.vy = (math.sqrt((obj.x1 - obj.x0)**2 + (obj.y0 - obj.y1)**2)*(2**0.5))*math.sin(obj.ticker)*math.sin(obj.an)
	obj.x1 = obj.x1 + obj.vx
	obj.y1 = obj.y1 + obj.vy
	if obj.ticker >= 0.3:
		obj.isMoving = False
		obj.vx = 0
		obj.vy = 0
		obj.x0 = 0
		obj.y0 = 0
		obj.x1 = obj.x*64
		obj.y1 = obj.y*64
		obj.ticker = 0
		obj.justEndedMoving = True

def AnimationUgol(obj):
	if obj.x1 - obj.x0 == 0:
		print(obj.y1, obj.y0)
		if obj.y1 >= obj.y0:
			obj.an = -math.pi / 2
		else:
			obj.an = math.pi / 2
	else:
		obj.an = math.atan((obj.y1 - obj.y0) / (obj.x1 - obj.x0))
	if -obj.x1 + obj.x0 < 0: obj.an += math.pi

def movin():
	pass