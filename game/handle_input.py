import pygame
from include.game.controls import NO_MOVE, UP, DOWN, LEFT, RIGHT


class InputHandler:


    def __init__(self):
        self.current_move = NO_MOVE
        pass
    
    def get_move(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return UP
                if event.key == pygame.K_DOWN:
                    return DOWN
                if event.key == pygame.K_LEFT:
                    return LEFT
                if event.key == pygame.K_RIGHT:
                    return RIGHT

        return NO_MOVE

    pass

