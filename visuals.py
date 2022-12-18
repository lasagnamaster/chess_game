import pygame, figures, math

ColorSpeed = 4
IsRotate = False
def IsGunRotate():
	global IsRotate
	IsRotate = True
def scale_down(obj, pic1, pic2, surf, desk):
	if obj.clicked and obj.allowedToMove:
		if not(obj.transformed):
			obj.s[0]-=4
			obj.s[1]-=4
			if obj.color == 1: obj.surf = pygame.transform.scale(pic1, (obj.s[0], obj.s[1]))
			elif obj.color == 0: obj.surf = pygame.transform.scale(pic2, (obj.s[0], obj.s[1]))

			if obj.s[0]<=50:
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
		obj.s = [64, 64]
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
	obj.vy = (math.sqrt((obj.x1 - obj.x0)**2 + (obj.y0 - obj.y1)**2)*(2**0.5))*math.sin(obj.ticker)* math.sin(obj.an)
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

def gun_move_and_rotate(obj, pic1):
	global IsRotate
	if obj.gun_trans == 255:
		obj.gun_trans = 255
	else:
		obj.gun_trans += 16
	gun_surf = pygame.Surface((256,256))
	gun_surf.set_colorkey((0,0,0))
	x0,y0 = pygame.mouse.get_pos()
	if IsRotate == True:
		if x0 == (obj.x1 + 284+32):
			if (y0- (obj.y1+104+32) )>= 0:
				an = -math.pi/2
			else:
				an = math.pi/2
		else:
			if (x0 - (obj.x1 +284+32)) >= 0:
				an = -math.atan((y0 - (obj.y1+104+32))/(x0-(obj.x1 + 284+32)))
			else:
				an = math.atan((y0 - (obj.y1+104+32))/(x0-(obj.x1 + 284+32)))
		new_rotate = pygame.transform.rotate(pic1, -an*180/math.pi)
		rotate_rect = new_rotate.get_rect(center =(128,128))
	gun_surf.set_alpha(obj.gun_trans)
	gun_surf.blit(new_rotate,rotate_rect)
	if (x0 - (obj.x1 + 284 + 32)) >= 0:
		gun_surf = pygame.transform.flip(gun_surf, True, False)
	return gun_surf

def AnimationUgol(obj):
	if obj.x1 - obj.x0 == 0:
		if obj.y1 >= obj.y0:
			obj.an = -math.pi / 2
		else:
			obj.an = math.pi / 2
	else:
		obj.an = math.atan((obj.y1 - obj.y0) / (obj.x1 - obj.x0))
	if -obj.x1 + obj.x0 < 0: obj.an += math.pi

if __name__ == "__main__":
    print('you were not supposed to use this as main')