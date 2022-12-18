import pygame

pygame.init()

figures_names = ['b_pawn.png', 'w_pawn.png', 'b_ladya.png', 'w_ladya.png', 
                    'b_bishop.png','w_bishop.png','b_horse.png','w_horse.png',
                    'b_queen.png','w_queen.png','b_king.png','w_king.png']
FIGURES_PICS = [pygame.image.load('images/figures/'+path) for path in figures_names]


visuals_names = ['clipart-2d-chess-set-chessboard-512x512-e3cb.png', 'green.png']
VISUALS_PICS = [pygame.image.load('images/visuals/'+path) for path in visuals_names]

shop_buttons_names = ['bishop_b.png','bishop_w.png','horse_b.png','horse_w.png', 
                        'ladya_b.png', 'ladya_w.png', 'pawn_b.png', 'pawn_w.png',
                        'queen_b.png', 'queen_w.png', 
                        'pawn_bw.png', 'ladya_bw.png', 'bishop_bw.png', 'horse_bw.png', 'queen_bw.png']
SHOP_BUTTON_PICS = [pygame.image.load('images/shop_buttons/'+path) for path in shop_buttons_names]

sounds_names = ['moving_piece1.wav','moving_piece2.wav','moving_piece3.wav','moving_piece4.wav','moving_piece5.wav', 'moving_piece6.wav',
                'piece_upgrade1.wav','piece_upgrade2.wav','piece_upgrade3.wav','piece_upgrade4.wav', 'piece_upgrade5.wav', 'piece_upgrade6.wav']
SOUNDS = [pygame.mixer.Sound('sounds/sfx/'+path) for path in sounds_names]

if __name__ == "__main__":
    print('you were not supposed to use this as main')