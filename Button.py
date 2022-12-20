import pygame, pics_loading
import config

SCREEN_HEIGHT = 100
SCREEN_WIDHT = 300
Menu = True
Finish = False
Pause_Menu = False
Is_New_Game = False
class Button():
    def __init__(self, x, y, image, under_mouse_image):
        self.image = image
        self.image1 = image
        self.image2 = under_mouse_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.screen = pygame.Surface((SCREEN_WIDHT, SCREEN_HEIGHT))
        self.x = x
        self.y = y
        self.clicked = False
    
    def draw(self, surf):
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.image, (0,0))
        if self.rect.collidepoint(pos):
            self.image = self.image2
        else:
            self.image = self.image1
        surf.blit(self.screen, (self.x, self.y))

class Start(Button):
    def __init__(self, x, y, image, under_mouse_image):
        super().__init__(x, y, image, under_mouse_image)

    def click(self):
        global Menu, Pause_Menu, Is_New_Game
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.image2
            print(self.clicked)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                Is_New_Game = True
                Menu = False
                Pause_Menu = False

class Resume(Button):
    def __init__(self, x, y, image, under_mouse_image):
        super().__init__(x, y, image, under_mouse_image)

    def click(self):
        global Menu, Pause_Menu
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.image2
            print(self.clicked)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                Menu = False
                Pause_Menu = False


class Quit(Button):
    def __init__(self, x, y, image, under_mouse_image):
        super().__init__(x, y, image, under_mouse_image)

    def click(self):
        global Menu, Finish
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
               self.clicked = True
               Finish = True

class Menu_Open(Button):
    def __init__(self, x, y, image, under_mouse_image):
        super().__init__(x, y, image, under_mouse_image)

    def click(self):
        global Menu, Finish
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                Menu = True

