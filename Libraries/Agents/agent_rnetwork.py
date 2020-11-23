
from Libraries.Structures.tetiomers         import O,L,N,Z,T,I,J
from Libraries.consts            import get_color, Colors
from Libraries.Algoritms.alg_nn            import NeuralNetwork


import pygame
import math
import copy
import datetime
import keras

from Libraries.vector import Vector
from random import uniform, randint

from Libraries.consts    import *

from statistics import mean, median
#from logs import CustomTensorBoard

class ReinforcmentNetwork:
    nn             = None
    last_action    = None
    rewards        = {}
    previous_state = [0,0,0,0]
    current_state  = [0,0,0,0]

    scores         = []

    def __init__(self):
        self.nn = NeuralNetwork( 4 )

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        mins = max( x_pos, 0)
        maxs = min( x_pos + 4, GRID_WIDTH)
        importantHeights = grid.heights[mins: maxs]
        pos_y = max( math.fabs(GRID_HEIGHT - max( importantHeights )) - 4, 0 )
        t.position[1] = int(pos_y)

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(grid), grid.clearedRow

    def evaulate(self, grid):
        return [ grid.maxColumn, 
                 grid.sumHeight, 
                 grid.sumHoles , 
                 grid.bumpiness#+ grid.clearedRow
                ]

    def next_move(self, t, grid, _unsed):
        grid = grid.get_grid()
        if self.last_action:
            self.nn.add_to_memory( self.previous_state, self.current_state, self.rewards[self.last_action], False )
            self.rewards = {}

        self.previous_state = self.current_state

    #    print( t ) 
        states = {}
        for j in range(0, t.max_rotate):
        #    print( range( t.get_position_range()[0], t.get_position_range()[1] + 1), t.current_rotate )
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1):
                t.position = [3,0]

                evaluation, reward = self.try_fit( i, t, grid.clone() )

                states[  ( i, t.current_rotate ) ] = evaluation
                self.rewards[ ( i, t.current_rotate ) ] = reward
            if t.can_rotate : t.rotate_left()

        t.position = [3,0]
       # print( states.keys() )
        best = self.nn.best_state(states)
      #  print( best )

        
        t.current_rotate =   best[1]
        t.position       = [ best[0], 0 ]

     #   print( "Selection is over")
    #    print( t.position, t.current_rotate)

        self.last_action = best
        self.current_state  = states[best]

        return 0


#    def next_move(self, tetromino, grid ) : 
#        state = [ grid.maxColumn, 
#                grid.sumHeight, 
#                grid.sumHoles , 
#                grid.bumpiness]
#        reward = grid.clearedRow
#        print( state, reward )
#        return 0

    def game_over_feedback(self, score, cleaned):
        self.nn.add_to_memory( self.previous_state, self.current_state, self.rewards[self.last_action], True )
        self.rewards        = {}
        self.previous_state = [0,0,0,0]
        self.current_state     = [0,0,0,0]
        self.last_action    = None

        self.scores.append( score )

        avg_score = mean(self.scores)
        min_score = min(self.scores)
        max_score = max(self.scores)

        print("New score :", score, "AVG :", avg_score, "MIN :", min_score, "MAX :", max_score)

    #    log.log(0, avg_score=avg_score, min_score=min_score,
    #                max_score=max_score)

        self.nn.train()