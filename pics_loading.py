import pygame

def figures_loading():
    figures_names = ['b_pawn.png', 'w_pawn.png', 'b_ladya.png', 'w_ladya.png', 
                     'b_bishop.png','w_bishop.png','b_horse.png','w_horse.png',
                     'b_queen.png','w_queen.png','b_king.png','w_king.png']
    figures_pics = [pygame.image.load('images/figures/'+path).convert_alpha() for path in figures_names]
    return figures_pics

def visuals_loading():
    visuals_names = ['clipart-2d-chess-set-chessboard-512x512-e3cb.png', 'green.png', 'Bazooka.png']
    visuals_pics = [pygame.image.load('images/visuals/'+path).convert_alpha() for path in visuals_names]
    return visuals_pics

def __main__():
    print('you were not supposed to use this as main')