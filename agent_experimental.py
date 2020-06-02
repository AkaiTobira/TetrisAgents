
from neural_network    import NeuralNetwork
from tetiomers         import O,L,N,Z,T,I,J
from consts            import get_color, Colors
from handler_structure import MultidimensionalDictionary
from tetris            import TetrisGrid 

import pygame
import math
import copy
import datetime
import pprint

from vector import Vector
from random import uniform, randint

from consts    import *

class PredifinedLearning:
    set_of_moves = None
    animation = []
    cold      = 0.99

    def __init__(self):
        self.moves = open("logs/exp/EXP_DICT_" + DATE_TIME, "w")
    #    self.set_of_moves = MultidimensionalDictionary( 5, (-2,-1, 0, 1, 2))
    #    self.fill()

    def __construct_height_array(self, bumpines):
        height   = [0]
        for g in range(len(bumpines)):
            height.append( height[g] - bumpines[g])
        smallest_h = min(height)
        for h in range( len( height)):
            height[h] -= smallest_h
        return height

    def __constuct_grid(self, height):
        grid = TetrisGrid()
        for g in range( len(height) ):
            for j in range( height[g] ):  grid[g][GRID_HEIGHT-j-1] = Colors.GOLD
        for g in range( len(height), GRID_WIDTH,1):
            for j in range( GRID_HEIGHT): grid[g][j] = Colors.GOLD
        #print( grid )
        return grid

    def __calculate_bumpines_abs_sum( self, height):
        abs_sum = 0
        for g in range( 0, len(height)-1 ):
            abs_sum += math.fabs(height[g] - height[g+1])
        return abs_sum  

    def __convert_tetromino_to_index(self, tetromino):
        if type(tetromino) == O : return 2
        if type(tetromino) == L : return 4
        if type(tetromino) == J : return 3
        if type(tetromino) == N : return 0
        if type(tetromino) == Z : return 1
        if type(tetromino) == T : return 5
        if type(tetromino) == I : return 6

    def __process_update(self, tetromino, grid, l_heights, pos ):
        tetromino.position = [3, 0]
        self.try_fit(pos, tetromino, grid)
    #    print( "Stuck in fir ")
        new_height = grid.heights[0: l_heights]
        abs_sum = self.__calculate_bumpines_abs_sum(new_height)
        #print( abs_sum )
        return - sum(new_height)#( abs_sum + sum(new_height) )

    def fill(self):
        return
        bumpines = [ -2, -2, -2, -2, -2]
        max_key_in_array    =  2 + 1
        lowest_key_in_array = -2

        COUNTER = 0
    #    print( "STart fill ")
        while bumpines[len( bumpines )-1] != max_key_in_array:
            #print( bumpines )
            if bumpines == [2,2,2,2,2]: break
            for index in range( len( bumpines )):
                print( COUNTER )
                COUNTER += 1
                
                height         = self.__construct_height_array(bumpines)
                grid           = self.__constuct_grid(height)
                abs_sum        = self.__calculate_bumpines_abs_sum(height)
                tetromino_list = [ O() ]# N(), Z(), O(), J(), L(), T(), I()]
    #            print( abs_sum )
                for tetromino in tetromino_list:
                    for rotation in range(tetromino.max_rotate):
    
                        move_worthness = self.set_of_moves._dict[ self.__convert_tetromino_to_index(tetromino) ][ tetromino.current_rotate ]
                        for key in bumpines:
                            move_worthness = move_worthness[key]

                        current_worthness  = sum(height) #+ abs_sum
                        #print( current_worthness )
                        possible_positions = [ tetromino.get_position_range()[0], tetromino.get_position_range()[0] + len(height) - tetromino.get_size()[2]]

                        for i in range(len(possible_positions)):
                            new_worthness = self.__process_update( tetromino, grid.clone(), len(height), possible_positions[i])
                        #    print( " WORTHNESS ", current_worthness, " : " ,  new_worthness )
                            move_worthness[i] = - new_worthness 

                        if tetromino.can_rotate : tetromino.rotate_left()



                bumpines[index] += 1
                if bumpines[index] == max_key_in_array and i != len(bumpines)-1:
                    bumpines[index] = lowest_key_in_array
                    print( "" )
                else: break    
                
        #p = pprint.PrettyPrinter()
        pprint.pprint(self.set_of_moves._dict, self.moves)


    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
       #     print( t.position )
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                break


    def validate(self, index, size, shape, grid, pos):
        if index + size[3] > GRID_HEIGHT: return False
        for k in range(size[0],size[2],1): 
            for l in range(size[1],size[3],1):
                if shape[k][l] and grid[pos + k][index + l]:  return False
        return True

    def reduce_by_smalest(self, array):
        smallest = min(array)
        for i in range(len(array)):
            array -= smallest
        return array

    def select_move( self, tetromino, grid):
        situation = []

        for values in range(len(grid.heights)-1):
            situation.append( grid.heights[values] - grid.heights[values+1] )

        self.animation = []
        best      = [ -1000, 0, 0]
        for i in range(tetromino.max_rotate):
            current = self.set_of_moves.get_value( tetromino, situation )

            if current >= best:
                self.animation = self.set_of_moves._memorised_sequence
                best      = current
            if tetromino.can_rotate : tetromino.rotate_left()

        tetromino.current_rotate =   best[1]
        tetromino.position       = [ best[2], 0 ]

    def select_bestMove(self, tetromino, grid ) : 
        self.select_move( tetromino, grid)

    #    print( tetromino.position, tetromino.current_rotate, type(tetromino) )

        score = self.simulate_move(  tetromino.position[0], tetromino, tetromino.current_rotate, grid )
        tetromino.is_locked = True
     #   print( self.animation)

        return score

    def set_score(self, score, number_of_tetrominos):
        self.cold *= 2

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