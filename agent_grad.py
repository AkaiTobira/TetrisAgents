import pygame
import math
import copy
import datetime

from vector import Vector
from random import uniform, randint

from consts    import *

class GradAi:
    current_values = None
    explore_chance = 0.5

    hights = [0,0,0,0,0,0,0,0,0,0]
    holes  = [0,0,0,0,0,0,0,0,0,0]

    def __init__(self):
        self.moves = open("logs/grd/GRD_MOV_" + DATE_TIME, "w")
        self.current_values = Vector(5)
        self.current_values.v = [-1,-1,-1,-4,0]

    def lock_tetromino(self, grid , t):
        shape_size = t.get_size()
        shape      = t.get_shape()
        pos        = t.position

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i] and grid[pos[0] + i][ pos[1] + j] == get_color(Colors.BLACK):
                    grid[pos[0] + i][ pos[1] + j] = t.color#get_color(Colors.GOLD)
    
    def unlock_tetromino(self, grid, t):
        shape_size = t.get_size()                 
        shape      = t.get_shape()            
        pos        = t.position                               

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i] and grid[pos[0] + i][ pos[1] + j] == get_color(Colors.GOLD): 
                    grid[pos[0] + i][ pos[1] + j] = get_color(Colors.BLACK)

    def select_bestMove(self, t, grid):
        best_move = self.gradient_descent( grid, t )

        t.current_rotate =   best_move[1]
        t.position       = [ best_move[2][0], t.position[1] ]
        
        score = self.simulate_move(  best_move[2][0], t, best_move[1], grid )

        t.is_locked = True

        if self.explore_chance > 0.001:
            self.explore_chance = self.explore_chance * 0.99
        else : self.explore_chance = 0

        return score

    def set_score(self, score, cleaned): 
        self.evolution_alg.add_score(score, cleaned)
        self.current_values = self.evolution_alg.get_next_active()
    
    def evaulate(self, board):
        return (board.clearedRow + 
                board.maxColumn* self.current_values[0] +  
                board.sumHeight* self.current_values[0] + 
                board.sumHoles * self.current_values[0] +
                board.bumpiness* self.current_values[0] )

    def return_score(self, score, cleaned, s3 ="3"): 
        self.moves.write("#GAMEOVER#SCORE" + str(score) +"#" + str((cleaned/5.0))[:5] + "\n")
        pass

    def _first_heurestic_evaluation(self, grid):
        self.hights = [0,0,0,0,0,0,0,0,0,0]
        self.holes  = [0,0,0,0,0,0,0,0,0,0]

        i = 0 
        while i < GRID_WIDTH:
            for j in range( 0, GRID_HEIGHT ):
                if grid[i][j] != get_color(Colors.BLACK): 
                    self.hights[i]  = abs( GRID_HEIGHT - j )
                    break
            i += 1

        for i in range(GRID_WIDTH):
            for j in range( 0, GRID_HEIGHT-1, 1):
                if grid[i][j] != get_color(Colors.BLACK) and grid[i][j+1] == get_color(Colors.BLACK):
                    self.holes[i] += 1    

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

    def evaluate_heurestisc(self, t, grid):
        heights    = self.hights.copy()
        holes      = self.holes.copy()

        height_sum = 0
        full_rows  = 0
        bumpiness  = 0
        hole       = 0

        i = 0 
        while i < GRID_WIDTH:
            for j in range( 0, GRID_HEIGHT ):
                if grid[i][j] != get_color(Colors.BLACK): 
                    heights[i]  = abs( GRID_HEIGHT - j )
                    break
            i += 1

        full_rows = self.clear_full_rows( t.position, t.get_size(), grid)
        for i in range( GRID_WIDTH ): heights[i] -= full_rows
    
        for i in range(GRID_WIDTH):
            holes[i] = 0
            for j in range( 0, GRID_HEIGHT-1, 1):
                if grid[i][j] != get_color(Colors.BLACK) and grid[i][j+1] == get_color(Colors.BLACK):
                    holes[i] += 1

        hole       = sum(holes)
        height_sum = sum(heights)
        max_height = max(heights)

        for i in range( 0, GRID_WIDTH ):
            if not i == 0: bumpiness += math.fabs( heights[i-1] - heights[i] )

        return ( height_sum * self.current_values[0] + 
                 max_height * self.current_values[1] + 
                 bumpiness  * self.current_values[2] + 
                 hole       * self.current_values[3] +
                 full_rows
                 )


    def find_best_move(self, t, grid ):

        if uniform( 0, 1) < self.explore_chance: #Select random move
            self.moves.write("#MOVE IS RANDOM#\n")
            print( "Move is random")
            return [ 0, randint(0, t.max_rotate-1), [ randint( t.get_position_range()[0], t.get_position_range()[1] ), 0 ] ]

        self._first_heurestic_evaluation(grid)

        best = [ -9999999.0, t.get_position_range()[0], 0]
        for j in range(0, t.max_rotate):
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1 ):
                t.position = [3,0]
                v = self.try_fit( i, t, self.copy_grid(grid))
            #    print( v, i, j )
                if v > best[0] : best = [v, i, t.current_rotate]
            if t.can_rotate : t.rotate_left()

        return [ best[0], best[2], [ best[1], 0 ]]

    def get_current_parameters(self, board):
        self._first_heurestic_evaluation(board)
        
        h_sum        = sum(self.hights)
        h_holes      = sum(self.holes)
        h_max_height = max(self.hights)
        h_bump       = 0

        for i in range( len(self.hights)-1 ):
            h_bump += abs( self.hights[i+1] - self.hights[i] )

        return [h_sum,  h_bump, h_max_height, h_holes, 0]

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos
        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                self.lock_tetromino(grid,t)
                heurestics = self.evaluate_heurestisc(t, grid)
        #        self.unlock_tetromino(grid,t)
                return heurestics

    def copy_grid(self, grid):
        logic_grid = []
        for i in range(GRID_WIDTH):
            logic_grid.append([])
            for j in range(GRID_HEIGHT):
                logic_grid[i].append(  get_color(Colors.BLACK) if grid[i][j] == get_color(Colors.BLACK) else get_color(Colors.GOLD) ) 
        return logic_grid

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

    def weight_callibration(self, o_param, n_param, reward):
        alpha = 0.001
        gamma = 0.99

        self.moves.write("#VALUE#SBEFORE#CALIBRTIONS#" + str(self.current_values))

        for i in range( len( self.current_values.v) ):
            self.current_values[i] = self.current_values[i] + alpha * self.current_values[i] * ( reward - o_param[i] + gamma * n_param[i])

        #print( self.current_values )

        regularization = abs(sum(self.current_values))

        #regularization = 1
        #print( regularization )

        self.current_values /= regularization

        print( self.current_values.min_normalization(),self.current_values.norm())
        #for i in range(0, len(self.current_values)):
        #    self.current_values[i] = self.current_values[i] / regularization

        #print( self.current_values )

        for i in range(0, len(self.current_values.v)):
            self.current_values[i] = math.floor(1e4 * self.current_values[i]) / 1e4
        self.moves.write("#VALUES#After#CALIBRTIONS#" + str(self.current_values) + "\n")
        #print( self.current_values )

    def gradient_descent(self, board, falling_piece):
        self.current_values
        self.explore_chance

        self.moves.write( "#" + str(self.explore_chance) + "#" + str(self.current_values) + "#\n")
        #print( "before ::: UPdATE", self.current_values, self.explore_chance )

        move = self.find_best_move( falling_piece, copy.deepcopy(board) )

        #print( " Calculated_bestMove " )

        current_parameters = self.get_current_parameters(board)

        #print( "Get_Old_Params")

        test_board         = self.copy_grid(board)

        #print( "Copied" )



        score              = self.simulate_move( move[2][0], falling_piece, move[1], test_board )



        new_parameters     = self.get_current_parameters(test_board) 
        new_parameters[4]  = score

        self.moves.write( "CLEANED" + str(score) + "\n")

        #print( "Get_allParams")

        step_reward = 5 * ( score * score ) - ( new_parameters[0] - current_parameters[0])

        self.moves.write( "STEPREWARD" + str(step_reward ) + "\n")

        self.weight_callibration( current_parameters, new_parameters, step_reward )

        #print( "after :::: UPdATE", self.current_values, self.explore_chance )

        return move
