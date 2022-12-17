import pygame, figures, pics_loading, random

class Shop_button():
    def __init__(self, pic, pic1, pic_blocked, figure, x = 0, y = 0):
        self.pic = ''
        self.x = x
        self.y = y
        self.pic = [pic, pic1, pic_blocked]
        self.surf = pygame.Surface((64,64))
        self.blocked = True
        self.figure = figure
        self.figureClicked = None
        self.rect = pic.get_rect(topleft = (x, y))

    def draw(self, nameOfTheColor, coins):

        payment = self.figure.payment
        self.blocked = True

        if nameOfTheColor == 1 and coins[1] >= payment: self.blocked = False
        elif nameOfTheColor == 0 and coins[0] >= payment: self.blocked = False 
        
        if self.blocked:
            self.surf.blit(self.pic[2], (0,0))
        else:
            if nameOfTheColor == 1:
                self.surf.blit(self.pic[0], (0,0))
            else:
                self.surf.blit(self.pic[1], (0,0))
        return self.surf

    def click(self, figurs, coins, nameOfTheColor):
        pos = pygame.mouse.get_pos()
        figureClicked = self.figureClicked
        payment = self.figure.payment
        areWeKillingTheKing = False
        if figureClicked!=None:
            for f in figurs[0].figures:
                if f.color==figureClicked and type(f)==King:
                    f.goes(desk)
                    attackingFigures = f.attackingFigures
                    print(attackingFigures)
                    if f.underAttack: 
                        areWeKillingTheKing = True
        if self.rect.collidepoint(pos) and figureClicked!=None and type(figureClicked)!=figures.King and not(areWeKillingTheKing) and figureClicked.color == nameOfTheColor:
            if not(type(figureClicked)==type(self.figure)):
                if type(self.figure) == figures.Pawn:
                    figurs.append(figures.Pawn(x = figureClicked.x, y = figureClicked.y, color = figureClicked.color))
                elif type(self.figure) == figures.Ladya:
                    figurs.append(figures.Ladya(x = figureClicked.x, y = figureClicked.y, color = figureClicked.color))
                elif type(self.figure) == figures.Horse:
                    figurs.append(figures.Horse(x = figureClicked.x, y = figureClicked.y, color = figureClicked.color))
                elif type(self.figure) == figures.Bishop:
                    figurs.append(figures.Bishop(x = figureClicked.x, y = figureClicked.y, color = figureClicked.color))
                elif type(self.figure) == figures.Queen:
                    figurs.append(figures.Queen(x = figureClicked.x, y = figureClicked.y, color = figureClicked.color))
                if figureClicked.color == 0:
                    coins[0]-=payment
                else:
                    coins[1]-=payment
                pics_loading.SOUNDS[random.randint(5, 8)].play()
                figurs.remove(figureClicked)
                self.figureClicked = None
           

