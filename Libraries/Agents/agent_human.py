
from Libraries.consts import *

class HumanPlayer:
    def __init__(self): pass

    def next_move(self, t, logic_grid, event): 
        if event.type == pygame.KEYUP:
            if event.key == AppKeys.RotateLeft:
                logic_grid.rotate_left(t)
            if event.key == AppKeys.RotateRight:
                logic_grid.rotate_right(t)
            if event.key == AppKeys.MoveRight:
                logic_grid.move_right(t)
            if event.key == AppKeys.MoveLeft:
                logic_grid.move_left(t)
            if event.key == AppKeys.DropDown:
                logic_grid.drop(t)
        return 0

    def game_over_feedback(self, score, number_of_tetrominos): pass