
import re
from Libraries.Structures.logger import LoggerInstance
from Libraries.Structures.meansures import Meansures
from Libraries.Structures.settings     import *
from Libraries.Structures.tetiomers         import O,L,N,Z,T,I,J
from Libraries.consts            import get_color, Colors, DATE_TIME, RANGE_0_GRID_HEIGHT, RANGE_0_GRID_WIDTH
from Libraries.Algoritms.alg_nn2            import NeuralNetwork2, NeuralNetworkFixed2
from Libraries.Structures.best_saver import BestUnitsBackupSaver, BestUnitSaver

import pygame
import math
import copy
import datetime
import keras

import datetime

from Libraries.vector import Vector
from random import uniform, randint

from Libraries.consts    import *

from statistics import mean, median
#from logs import CustomTensorBoard

class ReinforcmentNetwork2:
    nn             = None
    last_action    = None
    rewards        = {}
    fill_grid      = 0
    previous_state = [0,0,0,0,0,0]
    current_state  = [0,0,0,0,0,0]
    spawnerType    =  -1
    scores         = []


    def __init__(self, loadedModel = None,):
        if( loadedModel == None): self.nn = NeuralNetwork2()
        else: self.nn = NeuralNetworkFixed2( loadedModel )
        Meansures.register_meansure("GenerationProcessingNN" + str(PARAMS.GENERATOR))

    holes = 0

    def get_tetrimino_binart(self, t):
        rotations = []

        if t.current_rotate == 0 : rotations = [1,0,0,0]
        elif t.current_rotate == 1 : rotations = [0,1,0,0]
        elif t.current_rotate == 2 : rotations = [0,0,1,0]
        elif t.current_rotate == 3 : rotations = [0,0,0,1]

        ids = []

        if t.m_id == 1 :    ids = [1,0,0,0,0,0,0]
        elif t.m_id == 2 :  ids = [0,1,0,0,0,0,0]
        elif t.m_id == 3 :  ids = [0,0,1,0,0,0,0]
        elif t.m_id == 4 :  ids = [0,0,0,1,0,0,0]
        elif t.m_id == 5 :  ids = [0,0,0,0,1,0,0]
        elif t.m_id == 6 :  ids = [0,0,0,0,0,1,0]
        elif t.m_id == 7 :  ids = [0,0,0,0,0,0,1]

        return rotations + ids

    def fill_percentage(self, grid):

        fill_percents = 0.0
        dictr = {}

        for j in RANGE_0_GRID_HEIGHT:
            dictr[j] = 0

        for i, row in enumerate( grid ):
            for j in RANGE_0_GRID_HEIGHT:
                dictr[j] += 0 if row[j] == 0 else 1

        for i in RANGE_0_GRID_HEIGHT:
            fill_percents += dictr[i] * i * i

        #print(dictr, fill_percents)

        return fill_percents / 33110.0
        





    def next_move(self, t, grid, _unsed):
        grid = grid.get_grid()
        if self.last_action:
            self.nn.add_to_memory( self.previous_state, self.current_state, self.rewards[self.last_action], False )
            self.rewards = {}

        self.previous_state = grid.to_int_list() + self.get_tetrimino_binart(t)
        self.holes = grid.sumHoles2

        states = {}
        for j in range(0, t.max_rotate):
        #    print( range( t.get_position_range()[0], t.get_position_range()[1] + 1), t.current_rotate )
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1):
                t.position = [3,0]

                bin_grid, reward, holes2, grid_percentage, higt = self.try_fit( i, t, grid.clone() )
                states[  ( i, t.current_rotate, t.position[1] ) ] = bin_grid + self.get_tetrimino_binart(t)


                fill_grid2 = (self.fill_grid + (4 * (t.position[1] / GRID_HEIGHT)) )/len(bin_grid)



                #print(grid_percentage)

                self.rewards[ ( i, t.current_rotate, t.position[1] ) ] = fill_grid2 #grid_percentage  + reward
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
        self.fill_grid += 4 
        self.holes = grid.sumHoles2

        return 0

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD), evaluate_immidetly = False)

                binary_grid = grid.to_int_list()
                grid_percentage = self.fill_percentage(grid)
                clearedRow  = grid.clear_full_rows(t.position, t.get_size())
                grid.evaluate_holes()
                grid.evaluate_hight()

                return binary_grid, clearedRow, grid.sumHoles2, grid_percentage, (200 - grid.sumHeight)/200



    bestScore = 0

    improve_counter = 0

    def game_over_feedback(self, score, cleaned):
        if self.nn.IS_LEARNABLE == False: return 

        self.nn.add_to_memory( self.previous_state, self.current_state, self.rewards[self.last_action], True )
        self.rewards        = {}
        self.previous_state = []
        self.current_state  = []
        self.last_action    = None
        self.fill_grid      = 0
        self.holes = 0

        sss = score * ROW_MULTIPLER + cleaned

        time = Meansures.get_meansure("GenerationProcessingNN" + str(PARAMS.GENERATOR))
        if sss > self.bestScore:
            BestUnitsBackupSaver.saveNeuralNetwork( self.nn, score )
            self.bestScore = sss
            LoggerInstance.log(self.nn.file_save_name, str(self.improve_counter)   + "," + str(time) + "," + str(self.bestScore)  )
            print(str(self.improve_counter)   + "," + str(time) + "," + str(self.bestScore))
            self.improve_counter = -1
            PARAMS.LEARNING_STATUS = int(cleaned/PARAMS.MAX_POINTS * 100)
            if cleaned == 100 :
                print("Complete : ",self.nn.NAME)
                event = pygame.event.Event(pygame.KEYUP, key=pygame.K_m)
                pygame.event.post(event)

        self.improve_counter += 1

        if self.improve_counter > 100000:
            score = self.bestScore - (int(self.bestScore/ROW_MULTIPLER) * ROW_MULTIPLER)
            PARAMS.LEARNING_STATUS = int(score/PARAMS.MAX_POINTS) * 100
            print("Complete : ",self.nn.NAME)
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_m)
            pygame.event.post(event)


        self.nn.train()
