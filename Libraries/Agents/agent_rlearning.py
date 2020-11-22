
from Libraries.Algoritms.neural_network    import NeuralNetwork
from Libraries.Structures.tetiomers         import O,L,N,Z,T,I,J
from Libraries.consts            import get_color, Colors
from Libraries.handler_structure import MultidimensionalDictionary

import pygame
import math
import copy
import datetime
import keras

from Libraries.vector import Vector
from random import uniform, randint

from Libraries.consts    import *

class ReinforcmentLearning:
    nn = None
    animation = []
    cold      = 0.5

    def __init__(self): pass
    #    self.nn = MultidimensionalDictionary( 4, (-5,-4,-3,-2,-1, 0, 1, 2, 3,4,5))

    def select_move( self, tetromino, grid):
        situation = []

        #print( type(tetromino), tetromino.position, tetromino.current_rotate )

        for values in range(len(grid.heights)-1):
            situation.append( grid.heights[values] - grid.heights[values+1] )
        #print( situation, len(situation))
        self.animation = []
        best      = [ -1000, 0, 0]
        for i in range(tetromino.max_rotate):
            current = self.nn.get_value( tetromino, situation)
            #print(current)
            if current >= best:
                self.animation = self.nn._memorised_sequence
                best      = current
            if tetromino.can_rotate : tetromino.rotate_left()

        tetromino.current_rotate =   best[1]
        tetromino.position       = [ best[2], 0 ]

        #print( tetromino.position, tetromino.current_rotate)

    def select_random_move(self,tetromino, grid):
        situation = []

        #print( type(tetromino), tetromino.position, tetromino.current_rotate )

        for values in range(len(grid.heights)-1):
            situation.append( grid.heights[values] - grid.heights[values+1] )

        best = self.nn.get_random_value( tetromino, situation)
        self.animation = self.nn._memorised_sequence
        
        print( "Random best ",  best )

        tetromino.current_rotate =   best[1]
        tetromino.position       = [ best[2], 0 ]

    def next_move(self, tetromino, grid ) : 
        if uniform(0,1) < self.cold:
            print( self.cold, " is random")
            self.cold *= 0.99
            self.select_random_move(tetromino, grid)
        else : self.select_move( tetromino, grid)

        print( tetromino.position, tetromino.current_rotate, type(tetromino) )

        score = self.simulate_move(  tetromino.position[0], tetromino, tetromino.current_rotate, grid )

        tetromino.is_locked = True

        self.nn._memorised_sequence = self.animation
        print( self.animation)
        self.nn.update(score)

        return score

    def set_score(self, score, number_of_tetrominos):
        if score < 1000: self.cold = 0.5
        #self.cold = min( self.cold * 2, 0.5 ) 
        pass

    def simulate_move( self, x_pos,  t, rotation, board):
        t.position = [ x_pos, 0 ]

        while( t.current_rotate != rotation): t.rotate_left()

        while True:
            
            t.position[1] += 1

            #print( t.position, t.get_position_range(), t.current_rotate)

            if not t.is_valid(board):
                t.position[1] -= 1
                self.lock_tetromino(board,t)
                return self.clear_full_rows( t.position, t.get_size(), board )

    def lock_tetromino(self, grid , t):
        shape_size = t.get_size()
        shape      = t.get_shape()
        pos        = t.position

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i] and grid[pos[0] + i][ pos[1] + j] == get_color(Colors.BLACK):
                    grid[pos[0] + i][ pos[1] + j] = t.color#get_color(Colors.GOLD)

    def _check_row(self, j, grid):
        for i in range(GRID_WIDTH):
            if grid[ i ][ j ] == get_color(Colors.BLACK) : return False
        return True

    def find_rows_to_delete(self, pos, shape_size, grid):
        rows_to_delete = []
        for j in range(shape_size[1], shape_size[3], 1):
            if self._check_row(pos[1] + j, grid): rows_to_delete.append( pos[1] + j ) 
        return rows_to_delete

    def clear_full_rows(self, position, shape, grid):
        rows_to_delete = self.find_rows_to_delete(position, shape, grid)
        for i in range(len(rows_to_delete)):
            for j in range(GRID_WIDTH):
                del grid[j][rows_to_delete[i]]
                grid[j].insert(0,  get_color(Colors.BLACK) )
        return len(rows_to_delete)
