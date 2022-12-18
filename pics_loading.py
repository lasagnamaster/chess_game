import pygame
pygame.init()
figures_names = ['b_pawn.png', 'w_pawn.png', 'b_ladya.png', 'w_ladya.png',
                 'b_bishop.png','w_bishop.png','b_horse.png','w_horse.png',
                 'b_queen.png','w_queen.png','b_king.png','w_king.png']
FIGURES_PICS = [pygame.image.load('images/figures/'+path) for path in figures_names]

visuals_names = ['clipart-2d-chess-set-chessboard-512x512-e3cb.png', 'green.png', 'Bazooka.png', 'menu-back.png', 'background.png', 'menu_pause_background.png']
VISUALS_PICS = [pygame.image.load('images/visuals/'+path) for path in visuals_names]

button_names = ['start.png', 'start2.png', 'quit.png', 'quit2.png', 'menu.png', 'menu2.png', 'resume.png', 'resume2.png']
BUTTON_PICS = [pygame.image.load('images/buttons/' + path) for path in button_names]

music_names = ['menu1.mp3','menu2.mp3','menu3.mp3','game1.mp3','game2.mp3','game3.mp3','game4.mp3',]
MUSIC = ['music/' + path for path in music_names]
def __main__():
    print('you were not supposed to use this as main')