from random import uniform, randint, seed
from math   import sqrt
from copy   import deepcopy
import pygame
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME_PSO, ROW_MULTIPLER, COMMON_SEED
from Libraries.vector import Vector
from Libraries.Structures.backupCreator import Backup
from Libraries.Algoritms.particle import Particle
from Libraries.Structures.meansures import Meansures
from Libraries.Structures.logger import LoggerInstance
from Libraries.Structures.best_saver import BestUnitsBackupSaver, BestUnitSaver

from Libraries.Structures.settings import PARAMS, Params
class PSO:
    particles = []
    best_score = -999999
    best_pos   = None

    index           = 0
    iteration       = 0
    max_iteration   = 0.0
    numberOfPlayedGames = 0

    file_name_best = ""
    file_name_avg  = ""
    file_name_pop  = ""

    logs_registered = False
    dateTime        = ""

    NAME = ""

    def constuct_name(self):
        self.NAME  = "PSO" + str(PARAMS.HEURYSTIC_AMOUNT)
        self.NAME += "_SIZE" + str(PARAMS.POPULATION_SIZE)
        self.NAME += "_GEN" + str(PARAMS.GENERATOR)
        self.NAME += "_T" + str(PARAMS.MAX_POINTS)
        self.NAME += "_PER" + str(PARAMS.NUMBER_OF_GAMES)
        self.NAME += "_c1" + str(PARAMS.C1)
        self.NAME += "_c2" + str(PARAMS.C2)
        self.NAME += "_w" + str(PARAMS.W)

    def __init__(self):
        self.constuct_name()
        self.logs_registered = False
        self.particles = []
        Meansures.register_meansure("GenerationProcessingPSO" + str(PARAMS.GENERATOR))

        self.continueSyle = Backup.load_pso( self )

        if not self.continueSyle:
            seed(COMMON_SEED)
            self.dateTime = DATE_TIME
            self.best_pos = Vector(PARAMS.HEURYSTIC_AMOUNT)
            for _ in range( PARAMS.POPULATION_SIZE ): 
                self.particles.append( Particle(PARAMS.HEURYSTIC_AMOUNT) )
            self.index = 0
        

#        self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 

    def __str__(self):
        s = ""
        for i in range( PARAMS.POPULATION_SIZE ):
            s += "["+ str(i) + str( self.particles[i] )  + "]\n"
        return s

    def register_logs(self):
        self.file_name_best = self.NAME + "_best_change"
        self.file_name_avg  = self.NAME + "_avrg_change"
        self.file_name_pop  = self.NAME + "_populations"
        LoggerInstance.register_log( self.file_name_best, self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_avg,  self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_pop,  self.dateTime, "pso", continueSyle=self.continueSyle)

    def logInfo(self):
        if not self.logs_registered : 
            self.register_logs()
            self.logs_registered = True

        BestUnitsBackupSaver.saveScore(self.NAME, self.best_pos, self.best_score )

        score  = 0
        tetrim = 0
        
        for i in range( PARAMS.POPULATION_SIZE ):
            i_score  = int(self.particles[i].curr_score / ROW_MULTIPLER)
            score  += i_score
            tetrim += int(self.particles[i].curr_score) - (i_score*ROW_MULTIPLER)

        avrg = int(score/PARAMS.POPULATION_SIZE)*ROW_MULTIPLER + int(tetrim/PARAMS.POPULATION_SIZE)

        LoggerInstance.log( self.file_name_avg, str(self.iteration) + ", " + str(avrg) + ", " + str(Meansures.lap_meansure("GenerationProcessingPSO" + str(PARAMS.GENERATOR))))
        LoggerInstance.log( self.file_name_pop, str(self))
        LoggerInstance.log( self.file_name_pop, "#################################" )

    def logBest(self):
        if not self.logs_registered : 
            self.register_logs()
            self.logs_registered = True
        LoggerInstance.log( self.file_name_best, str(self.iteration) + ", " + str(self.best_pos) + ", " +  str(self.best_score))

    def get_next_to_check(self, score, cleaned):
        if self.numberOfPlayedGames < PARAMS.NUMBER_OF_GAMES:
            self.particles[self.index].curr_score += score * ROW_MULTIPLER + cleaned
            self.numberOfPlayedGames += 1
            return self.particles[self.index].pos_v
        self.numberOfPlayedGames = 0

        maxScore     = int(self.particles[self.index].curr_score / ROW_MULTIPLER)
        maxTetrimino = int((self.particles[self.index].curr_score - (maxScore*ROW_MULTIPLER)) / PARAMS.NUMBER_OF_GAMES)
        maxScore     = int(maxScore/PARAMS.NUMBER_OF_GAMES)
        newScore = maxScore * ROW_MULTIPLER + maxTetrimino

        self.particles[self.index].curr_score = newScore
        self.particles[self.index].update_best()

        if newScore > self.best_score: 
            self.best_score = newScore
            self.best_pos   = self.particles[self.index].pos_v
            self.logBest()
        
        newIneria = PARAMS.W
        newIneria -= float(maxTetrimino)/float(int(PARAMS.MAX_POINTS)) * PARAMS.W
        newIneria = max(newIneria, 0)
        print(maxTetrimino, float(maxTetrimino)/float(int(PARAMS.MAX_POINTS)),  newIneria)

        score = BestUnitsBackupSaver.getLastBestScore(self.NAME)
        tetrimino = (score - (int(score / ROW_MULTIPLER) * ROW_MULTIPLER))
        if tetrimino > PARAMS.MAX_POINTS: 
            PARAMS.LEARNING_STATUS = 100
            print("Complete : ",self.NAME)
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_m)
            pygame.event.post(event)

        self.particles[self.index].move(self.best_pos, newIneria, PARAMS.C1, PARAMS.C2)
        #print(str(self.index) + " " + str(self.particles[self.index]))

        self.index += 1
        if self.index == PARAMS.POPULATION_SIZE: 
            self.index = 0
            self.iteration += 1
            #if self.ineria < 0.001 : self.ineria = 0
            #else : self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 
            print( "Iteration ", self.iteration, " out of ", self.max_iteration)
            self.logInfo()

        Backup.save_pso(self)

        self.particles[self.index].curr_score = 0
        #print(str(self.index) + " " + str(self.particles[self.index]))
        return self.particles[self.index].pos_v
