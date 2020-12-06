
from Libraries.consts import *
from copy import deepcopy
import math
import time

class TetrisGrid:
    grid = []

    heights    = [0,0,0,0,0,0,0,0,0,0]
    holes      = [0,0,0,0,0,0,0,0,0,0]


    biggestWheel = 0
    clearedRow   = 0
    maxColumn    = 0
    sumHeight    = 0
    sumHoles     = 0
    bumpiness    = 0

    def __init__(self, to_duplicate = None):
        self.grid = []
        for i in RANGE_0_GRID_WIDTH:
            row = []
            for j in RANGE_0_GRID_HEIGHT:
                row.append( 0  if to_duplicate == None or to_duplicate.grid[i][j] == 0 else 99 )
            self.grid.append(row)

        self.heights    = [0,0,0,0,0,0,0,0,0,0]
        self.holes      = [0,0,0,0,0,0,0,0,0,0]

    def clone(self):
        t = TetrisGrid( self )

        t.holes = self.holes.copy()
        t.heights = self.heights.copy()

        t.clearedRow = self.clearedRow
        t.maxColumn  = self.maxColumn
        t.sumHeight  = self.sumHeight
        t.sumHoles   = self.sumHoles
        t.bumpiness  = self.bumpiness
        t.biggestWheel = self.biggestWheel

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
            for j in RANGE_0_GRID_HEIGHT_M1:
                if row[j] != 0 and row[j+1] == 0:
                    self.holes[i] += 1

        self.maxColumn = max(self.heights)
        self.sumHeight = sum(self.heights)
        self.sumHoles  = sum(self.holes)
        self.bumpiness    = 0
        self.biggestWheel = 0

        bump_prev = 0
        bump      = 0
        for i in RANGE_0_GRID_WIDTH_M1:
            self.bumpiness += math.fabs( self.heights[i] - self.heights[i+1] )

            if i == 0:
                self.biggestWheel = self.heights[1] - self.heights[0]
            else:
                value =  (self.heights[i+1] + self.heights[i-1] - (2.0 *self.heights[i])) * 0.5
                self.biggestWheel = max( self.biggestWheel, value)

        self.biggestWheel = max( self.biggestWheel,  self.heights[8] - self.heights[9] )

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
