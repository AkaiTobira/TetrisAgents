import pygame

from Libraries.Structures.tetiomers  import *
from Libraries.Structures.grid_cell  import GridCell
from Libraries.consts     import *
from Libraries.Structures.displayers import ScoreDisplayer, NextTetiomerBox, HeuresticDisplayer
from Libraries.Structures.tetrominoSpawner import RandomSpawnTetromino

class TetrisGrid:
    grid = []

    heights    = [0,0,0,0,0,0,0,0,0,0]
    holes      = [0,0,0,0,0,0,0,0,0,0]

    clearedRow = 0
    maxColumn  = 0
    sumHeight  = 0
    sumHoles   = 0
    bumpiness  = 0

    def __init__(self, to_duplicate = None):
        self.grid = []
        for i in RANGE_0_GRID_WIDTH:
            row = []
            for j in RANGE_0_GRID_HEIGHT:
                row.append( 0  if to_duplicate == None or to_duplicate.grid[i][j] == 0 else 99 )
            self.grid.append(row)

    def clone(self):
        t = TetrisGrid( self )
        t.clearedRow = self.clearedRow
        t.maxColumn  = self.maxColumn
        t.sumHeight  = self.sumHeight
        t.sumHoles   = self.sumHoles
        t.bumpiness  = self.bumpiness
        return t        

    def __evaluate(self, tetromino):
        self.clearedRow = self.clear_full_rows(tetromino.position, tetromino.get_size())

        for i, row in enumerate( self.grid ):
            for j, value in enumerate( row ):
                if value != 0 :
                    self.heights[i] = abs( GRID_HEIGHT - j )
                    break

        for i, row in enumerate( self.grid ):
            self.holes[i] = 0
            for j in RANGE_0_GRID_WIDTH_M1:
                if row[j] != 0 and row[j+1] == 0:
                    self.holes[i] += 1

        self.maxColumn = max(self.heights)
        self.sumHeight = sum(self.heights)
        self.sumHoles  = sum(self.holes)
        self.bumpiness = 0

        for i in RANGE_0_GRID_WIDTH:
            if not i == 0: self.bumpiness += math.fabs( self.heights[i-1] - self.heights[i] )

    def lock(self, tetromino, color=(255,215,0)):
        shape_size = tetromino.get_size()
        shape      = tetromino.get_shape()
        pos        = tetromino.position

        if tetromino.is_locked : return

        rangeX = range(shape_size[0], shape_size[2])
        rangeY = range(shape_size[1], shape_size[3])

        for i in rangeX:
            posX = pos[0] + i
            for j in rangeY:
                if shape[j][i]: self.grid[posX][ pos[1] + j] = tetromino.m_id
        self.__evaluate(tetromino)

    def _check_row(self, j):
        for i in range(GRID_WIDTH):
            if self.grid[ i ][ j ] == 0 : return False
        return True

    def find_rows_to_delete(self, pos, shape_size):
        rows_to_delete = []
        for j in range(shape_size[1], shape_size[3], 1):
            if self._check_row(pos[1] + j): rows_to_delete.append( pos[1] + j ) 
        return rows_to_delete

    def clear_full_rows(self, position, shape):
        rows_to_delete = self.find_rows_to_delete(position, shape)
        for i, index in enumerate(rows_to_delete):
            for j in RANGE_0_GRID_WIDTH:
                del self.grid[j][index]
                self.grid[j].insert(0,  0 )
        return len(rows_to_delete)

    def remove_rows(self, rows_to_delete):
        for i, index in enumerate(rows_to_delete):
            for j in RANGE_0_GRID_WIDTH:
                del self.grid[j][index]
                self.grid[j].insert(0,  0 )

    def unlock( self, tetromino): pass

    def __str__(self):
        s = ""
        for j in range( GRID_HEIGHT):
            for i in range(GRID_WIDTH): 
                s += "1 " if self.grid[i][j] == 0 else "0 "
            s += "\n"
        return s

    def __getitem__(self, i):
        return self.grid[i]

    def __setitem__(self, i, c):
        self.grid[i] = c



#from agent_experimental import PredifinedLearning

import math
import time


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
            self.score += 1
            if self.logic_grid.clearedRow != 0 :
                self.score += (2 ** ( self.logic_grid.clearedRow -1 )) * ROW_MULTIPLER
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

class TetrisDisplayers:
    screen = None
    color  = get_color(Colors.LIGHT_PURPLE)
    points = None
    future = None
    grid   = None

    grid_position = [0, 0]

    enable_draw = True

    def __init__(self, screen, position):
        self.grid_position = position

        self.screen = screen
        self.points = ScoreDisplayer    (screen, [ position[0], position[1] + GRID_HEIGHT * SQUARE_SIZE  ])
        self.future = NextTetiomerBox   (screen, [ position[0], position[1] + GRID_HEIGHT * SQUARE_SIZE + GRID_WIDTH/2 * SQUARE_SIZE ])
        #self.heures = HeuresticDisplayer(screen, [ (GRID_WIDTH + 1) * SQUARE_SIZE + GRID_HEIGHT , (GRID_WIDTH/2  + 6) * SQUARE_SIZE ])

        self.grid = []
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append( GridCell( screen , ( (i * SQUARE_SIZE) + self.grid_position[0], (j * SQUARE_SIZE) + self.grid_position[1] )))

    def drawGrid(self):
        if not self.enable_draw: return
        for i in range(GRID_WIDTH*GRID_HEIGHT):
            self.grid[i].draw()	
    #    pygame.draw.rect(self.screen, self.color, [ self.grid_position[0] - OFFSET, self.grid_position[1] - OFFSET, (GRID_WIDTH * SQUARE_SIZE), (GRID_HEIGHT * SQUARE_SIZE) ], 2)	


    def draw(self):
        if not self.enable_draw: return 
        self.future.draw()
        self.points.draw()
    #    self.heures.draw()

    def process(self, event):
        if event.type == pygame.KEYUP:
            if event.key == AppKeys.SwichVisibility:
                self.enable_draw = not self.enable_draw

    def _convert_index(self, i, j):
        return i * GRID_HEIGHT + j

    def synchronize_grid(self, grid):
        if not self.enable_draw : return
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid[self._convert_index(i,j)].fill_cell( get_color( Colors(grid[i][j])))   

    def synchronize_numbers(self, score):
        #self.heures.process(heuresitcs, values)
        self.points.process(score)

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

