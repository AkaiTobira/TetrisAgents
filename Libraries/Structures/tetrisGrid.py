
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
    hTransitions = 0
    fullSquares  = 0
    avgHeight    = 0
    sumWheel     = 0
    bumpinessHeight = 0

    def __init__(self, to_duplicate = None):
        self.grid = []
        for i in RANGE_0_GRID_WIDTH:
            row = []
            for j in RANGE_0_GRID_HEIGHT:
                row.append( 0  if to_duplicate == None or to_duplicate.grid[i][j] == 0 else 99 )
            self.grid.append(row)

        self.heights     = [0,0,0,0,0,0,0,0,0,0]
        self.holes       = [0,0,0,0,0,0,0,0,0,0]

        self.clearedRow   = 0
        self.maxColumn    = 0
        self.sumHeight    = 0
        self.sumHoles     = 0
        self.avgHeight    = 0
        self.bumpiness    = 0
        self.biggestWheel = 0
        self.hTransitions = 0
        self.vTransitions = 0
        self.fullSquares  = 0
        self.sumWheel     = 0
        self.diffColumn   = 0
        self.minColumn    = 0
        self.maxColumn    = 0
        self.sumHoles2    = 0
        self.bumpinessHeight = 0

    def clone(self):
        t = TetrisGrid( self )

        t.holes = self.holes.copy()
        t.heights = self.heights.copy()

        t.clearedRow   = self.clearedRow
        t.maxColumn    = self.maxColumn
        t.sumHeight    = self.sumHeight
        t.avgHeight    = self.avgHeight
        t.sumHoles     = self.sumHoles
        t.sumHoles2    = self.sumHoles2
        t.bumpiness    = self.bumpiness
        t.biggestWheel = self.biggestWheel
        t.hTransitions = self.hTransitions
        t.fullSquares  = self.fullSquares
        t.sumWheel     = self.sumWheel
        t.vTransitions = self.vTransitions
        t.maxColumn  = self.maxColumn 
        t.minColumn  = self.minColumn
        t.diffColumn = self.diffColumn 
        t.bumpinessHeight = self.bumpinessHeight

        
        return t        

    def __evaluate(self, tetromino):
        self.clearedRow = self.clear_full_rows(tetromino.position, tetromino.get_size())
        self.hTransitions = 0
        self.fullSquares += (4 - self.clearedRow*GRID_WIDTH)

        for i, row in enumerate( self.grid ):
            for j, value in enumerate( row ):
                if value != 0 :
                    self.heights[i] = abs( GRID_HEIGHT - j )
                    break

        for i, row in enumerate( self.grid ):
            self.holes[i] = 0
            found = False
            for j in RANGE_0_GRID_HEIGHT_M1:
                value  = row[j]
                value2 = row[j+1]

                if value != 0: found = True
                if value == 0 and found: self.sumHoles2 += 1
                if value != 0 and value2 == 0:
                    self.holes[i] += 1
                    self.vTransitions += 1
                elif value == 0 and value2 != 0:
                    self.vTransitions += 1

        for i, row in enumerate( self.grid ):
            if i == GRID_WIDTH - 1: continue
            nextRow = self.grid[i+1]
            for j in RANGE_0_GRID_WIDTH_M1:
                if row[j] != 0 and nextRow[j] == 0:
                    self.hTransitions += 1
                elif row[j] == 0 and nextRow[j] != 0:
                    self.hTransitions += 1

        self.maxColumn  = max(self.heights)
        self.minColumn  = min(self.heights)
        self.diffColumn = self.maxColumn - self.minColumn
        self.sumHeight  = sum(self.heights)
        self.avgHeight  = self.sumHeight*0.1
        self.sumHoles   = sum(self.holes)
        self.bumpiness    = 0
        self.biggestWheel = 0
        self.sumWheel = 0


        self.bumpinessHeight  = (self.heights[0] - self.minColumn) * 5 + (self.heights[1] - self.minColumn) * 4 
        self.bumpinessHeight += (self.heights[2] - self.minColumn) * 3 + (self.heights[3] - self.minColumn) * 2 
        self.bumpinessHeight += (self.heights[4] - self.minColumn) * 1 + (self.heights[5] - self.minColumn) * 1 
        self.bumpinessHeight += (self.heights[6] - self.minColumn) * 2 + (self.heights[7] - self.minColumn) * 3 
        self.bumpinessHeight += (self.heights[8] - self.minColumn) * 4 + (self.heights[9] - self.minColumn) * 5 
        self.bumpinessHeight /= GRID_WIDTH
        #self.bumpinessHeight = (self.sumHeight - GRID_WIDTH*self.minColumn)/GRID_WIDTH

        for i in RANGE_0_GRID_WIDTH_M1:

            height_i = self.heights[i]
            height_i_1 = self.heights[i+1]

            self.bumpiness += math.fabs( height_i - height_i_1 ) 

            if i == 0:
                self.biggestWheel = self.heights[1] - self.heights[0]
                self.sumWheel += self.biggestWheel
            else:
                value =  (height_i_1 + self.heights[i-1] - (2.0 *height_i)) * 0.5
                self.biggestWheel = max( self.biggestWheel, value)
                self.sumWheel += value

        value2 = self.heights[8] - self.heights[9]
        self.biggestWheel = max( self.biggestWheel,  value2 )
        self.sumWheel += value2

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
