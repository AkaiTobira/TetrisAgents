import pygame

from Libraries.Structures.tetiomers  import *
from Libraries.Structures.grid_cell  import GridCell
from Libraries.consts     import *
from Libraries.Structures.displayers import ScoreDisplayer, NextTetiomerBox, HeuresticDisplayer
from Libraries.Structures.tetrominoSpawner import RandomSpawnTetromino
from Libraries.Structures.tetrisGrid import TetrisGrid


class TetrisLogic:
    logic_grid      = None
    score           = 0
    def __init__(self):
        self.reset()

    def reset(self):
        self.score      = 0
        self.logic_grid = TetrisGrid()

    def get_grid(self): return self.logic_grid   

    def progress_tetromino(self, tetromino):
        tetromino.position[1] += 1
        if not tetromino.is_valid(self.logic_grid):
            tetromino.position[1] -= 1
            self.logic_grid.lock(tetromino, tetromino.color)
        #    self.score += 1
            if self.logic_grid.clearedRow != 0 :
                self.score += (2 ** ( self.logic_grid.clearedRow -1 ))
                self.logic_grid.clearedRow = 0
            return False
        return True

    def move_left(self, tetromino):
        if tetromino.position[0] > tetromino.get_position_range()[0]  :
            tetromino.position[0] -= 1
            if not tetromino.is_valid(self.logic_grid) : tetromino.position[0] += 1

    def rotate_right(self, tetromino):
        if tetromino.can_rotate:
            tetromino.rotate_right()

    def move_right(self, tetromino):
        if tetromino.position[0] < tetromino.get_position_range()[1]  :
            tetromino.position[0] += 1
            if not tetromino.is_valid(self.logic_grid) : tetromino.position[0] -= 1
        
    def rotate_left(self, tetromino):
        if tetromino.can_rotate:
            tetromino.rotate_left()

    def drop( self, tetromino):
        while self.progress_tetromino(tetromino): pass
        tetromino.is_locked = True

    def game_over(self):
        for i in range(GRID_WIDTH):
            if self.logic_grid[ i ][ 1 ] != 0 : return True
        return False

#TODO add chaging beetween stats and score
class TetrisDisplayers:
    screen = None
    color  = get_color(Colors.LIGHT_PURPLE)
    points = None
    future = None
    grid   = None

    grid_position = [0, 0]

    enable_draw       = True
    enable_draw_stats = True 

    def __init__(self, screen, position, grid):
        self.grid_position = position

        self.screen = screen
        self.points = ScoreDisplayer    (screen, [ position[0], position[1] + GRID_HEIGHT * SQUARE_SIZE + 27 ])
        self.future = NextTetiomerBox   (screen, [ position[0], position[1] + GRID_HEIGHT * SQUARE_SIZE + GRID_WIDTH/2 * SQUARE_SIZE ])
        self.heures = HeuresticDisplayer(screen, [ position[0], position[1] + GRID_HEIGHT * SQUARE_SIZE  ], grid)

        self.grid = []
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append( GridCell( screen , ( (i * SQUARE_SIZE) + self.grid_position[0], (j * SQUARE_SIZE) + self.grid_position[1] )))

    def drawGrid(self):
        if not self.enable_draw: return
        for i in range(GRID_WIDTH*GRID_HEIGHT):
            self.grid[i].draw()	
    #    pygame.draw.rect(self.screen, self.color, [ self.grid_position[0] - OFFSET, self.grid_position[1] - OFFSET, (GRID_WIDTH * SQUARE_SIZE), (GRID_HEIGHT * SQUARE_SIZE) ], 2)	

    def setGrid(self, grid):
        self.heures.grid = grid 

    def draw(self):
        if not self.enable_draw: return 
        self.future.draw()
        self.points.draw()
        if self.enable_draw_stats : self.heures.draw()

    def process(self, event):
        if event.type == pygame.KEYUP:
            if event.key == AppKeys.SwichVisibility:
                self.enable_draw = not self.enable_draw
            if event.key == AppKeys.ToggleStatsDraw:
                self.enable_draw_stats = not self.enable_draw_stats

    def _convert_index(self, i, j):
        return i * GRID_HEIGHT + j

    def synchronize_grid(self, grid):
        if not self.enable_draw : return
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid[self._convert_index(i,j)].fill_cell( get_color( Colors(grid[i][j])))   

    def synchronize_numbers(self, lines, tetriminos):
        self.points.process(str(lines) + " | " + str(tetriminos))

    def synchronize_tetromino(self, c_t , n_t):
        self._draw_tetromino_in_grid(c_t)
        self.future.process(n_t)
        
    def _draw_tetromino_in_grid(self, c_t):
        shape_size = c_t.get_size()
        shape      = c_t.get_shape()
        pos        = c_t.position

        if c_t.is_locked : return

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i]: self.grid[self._convert_index(pos[0] + i, pos[1] + j)].fill_cell( c_t.color)

