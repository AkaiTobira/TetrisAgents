
from Libraries.Structures.logger import LoggerInstance
from Libraries.Structures.meansures import Meansures
from Libraries.Structures.settings     import *
from Libraries.Structures.tetiomers         import O,L,N,Z,T,I,J
from Libraries.consts            import get_color, Colors, DATE_TIME
from Libraries.Algoritms.alg_nn            import NeuralNetwork, NeuralNetworkFixed
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

class ReinforcmentNetwork:
    nn             = None
    last_action    = None
    rewards        = {}
    previous_state = [0,0,0,0,0,0]
    current_state  = [0,0,0,0,0,0]
    spawnerType    =  -1
    scores         = []


    def __init__(self, loadedModel = None,):
        if( loadedModel == None): self.nn = NeuralNetwork()
        else: self.nn = NeuralNetworkFixed( loadedModel )
        Meansures.register_meansure("GenerationProcessingNN" + str(PARAMS.GENERATOR))

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(t, grid), grid.clearedRow

    def evaulate(self, t, grid):
        heuristicList = []
        if CLEARED_ROW_INDEX      in PARAMS.HEURYSTIC: heuristicList.append(grid.clearedRow)
        if MIN_COLUMN_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.minColumn)
        if MAX_COLUMN_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.maxColumn)
        if DIFF_COLUMN_INDEX      in PARAMS.HEURYSTIC: heuristicList.append(grid.diffColumn)
        if SUM_HEIGHT_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHeight)
        if AVG_HEIGHT_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.avgHeight)
        if SUM_HOLES_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHoles2)
        if SUM_HOLES2_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHoles)
        if BUMPINESS_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.bumpiness)
        if BUMPINESS_HEIGHT_INDEX in PARAMS.HEURYSTIC: heuristicList.append(grid.bumpinessHeight)
        if H_TRANSITIONS_INDEX    in PARAMS.HEURYSTIC: heuristicList.append(grid.hTransitions)
        if V_TRANSITIONS_INDEX    in PARAMS.HEURYSTIC: heuristicList.append(grid.vTransitions)
        if BIG_WHEEL_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.biggestWheel)
        if SUM_WHEELS_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumWheel)
        if FULL_SQUARES_INDEX     in PARAMS.HEURYSTIC: heuristicList.append(grid.fullSquares)
        if TETRIMINO_POSITION     in PARAMS.HEURYSTIC: heuristicList.append(t.position[1])
        return heuristicList

    fill_grid = 0

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
                self.rewards[ ( i, t.current_rotate ) ] = reward  + (self.fill_grid + 4)/220
            if t.can_rotate : t.rotate_left()

        t.position = [3,0]
       # print( states.keys() )
        best = self.nn.best_state(states)
      #  print( best )

        
        t.current_rotate =   best[1]
        t.position       = [ best[0], 0 ]
        self.fill_grid += 4

     #   print( "Selection is over")
    #    print( t.position, t.current_rotate)

        self.last_action = best
        self.current_state  = states[best]

        return 0

    bestScore = 0

    improve_counter = 0

    def game_over_feedback(self, score, cleaned):
        if self.nn.IS_LEARNABLE == False: return 

        self.nn.add_to_memory( self.previous_state, self.current_state, self.rewards[self.last_action], True )
        self.rewards        = {}
        self.previous_state = [0,0,0,0,0,0]
        self.current_state  = [0,0,0,0,0,0]
        self.last_action    = None
        self.fill_grid      = 0

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

        #print("New score :", score, "cleaned :", cleaned, "Best Score :", self.bestScore)
        self.nn.train()
