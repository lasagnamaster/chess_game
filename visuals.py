import pygame, figures

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
		if obj.color == 1: obj.surf.blit(pic1,(0,0))
		else: obj.surf.blit(pic2,(0,0))
		obj.sx = 64
		obj.sy = 64
		obj.transformed = False 

def movin():
	pass