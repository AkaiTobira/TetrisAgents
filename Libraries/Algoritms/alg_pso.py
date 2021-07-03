from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME_PSO, ROW_MULTIPLER
from Libraries.vector import Vector
from Libraries.Structures.backupCreator import Backup
from Libraries.Algoritms.particle import Particle
from Libraries.Structures.meansures import Meansures
from Libraries.Structures.logger import LoggerInstance
from Libraries.Structures.best_saver import BestUnitsBackupSaver, BestUnitSaver

class PSO:
    particles = []
    best_score = -999999
    best_pos   = None

    NUMBER_OF_PLAYED_GAMES = 5
    POPULATION_SIZE = 0
    index           = 0
    iteraiton       = 0
    max_iteration   = 0.0
    numberOfPlayedGames = 0

    ineria     = 0.9

    congnitive_c = 0
    social_c     = 0

    file_name_best = ""
    file_name_avg  = ""
    file_name_pop  = ""

    VECTOR_DIMENSIONS = 7

    logs_registered = False
    dateTime        = ""
    spawnerId = 2

    def __init__(self, vector_dimensions, population_size, c1, c2, w):
        self.logs_registered = False
        self.VECTOR_DIMENSIONS = vector_dimensions
        self.POPULATION_SIZE = population_size
        self.max_iteration   = 1000
        self.particles = []
        self.spawnerId = 2
        Meansures.register_meansure("GenerationProcessingPSO" + str(2))

        self.congnitive_c = c1
        self.social_c = c2
        self.ineria = w

        self.continueSyle, self.particles, self.iteraiton, self.dateTime, self.index, self.best_pos, self.best_score = Backup.load_pso( self.VECTOR_DIMENSIONS, self.POPULATION_SIZE, 2, self.congnitive_c, self.social_c, self.ineria)

        if not self.continueSyle:
            self.dateTime = DATE_TIME
            self.best_pos = Vector(vector_dimensions)
            for _ in range( self.POPULATION_SIZE ): 
                self.particles.append( Particle(vector_dimensions) )
            self.index = 0

#        self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 

    def __str__(self):
        s = ""
        for i in range( len(self.particles) ):
            s += "["+ str(i) + str( self.particles[i] )  + "]\n"
        return s

    def register_logs(self):
        self.file_name_best = "PSO" + str(self.VECTOR_DIMENSIONS) + "_" + str(self.spawnerId) + "_c1-" + str(self.congnitive_c) + "_c2-" + str(self.social_c) + "_w-" + str(self.ineria) + "_P" + str(self.POPULATION_SIZE) + "_best_change"
        self.file_name_avg  = "PSO" + str(self.VECTOR_DIMENSIONS) + "_" + str(self.spawnerId) + "_c1-" + str(self.congnitive_c) + "_c2-" + str(self.social_c) + "_w-" + str(self.ineria) + "_P" + str(self.POPULATION_SIZE) + "_avrg_change"
        self.file_name_pop   ="PSO" + str(self.VECTOR_DIMENSIONS) + "_" + str(self.spawnerId) + "_c1-" + str(self.congnitive_c) + "_c2-" + str(self.social_c) + "_w-" + str(self.ineria) + "_P" + str(self.POPULATION_SIZE) + "_populations"
        LoggerInstance.register_log( self.file_name_best, self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_avg,  self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_pop,  self.dateTime, "pso", continueSyle=self.continueSyle)

    def logInfo(self):
        if not self.logs_registered : 
            self.register_logs()
            self.logs_registered = True

        BestUnitsBackupSaver.saveScore("PSO" + str(self.VECTOR_DIMENSIONS) + "_" + str(self.spawnerId) + "_c1-" + str(self.congnitive_c) + "_c2-" + str(self.social_c) + "_w-" + str(self.ineria) + "_P" + str(self.POPULATION_SIZE), self.best_pos, self.best_score )

        score  = 0
        tetrim = 0
        
        for i in range( self.POPULATION_SIZE ):
            i_score  = int(self.particles[i].curr_score / ROW_MULTIPLER)
            score  += i_score
            tetrim += int(self.particles[i].curr_score) - (i_score*ROW_MULTIPLER)

        avrg = int(score/self.POPULATION_SIZE)*ROW_MULTIPLER + int(tetrim/self.POPULATION_SIZE)

        LoggerInstance.log( self.file_name_avg, str(self.iteraiton) + ", " + str(avrg) + ", " + str(Meansures.lap_meansure("GenerationProcessingPSO" + str(self.spawnerId))))
        LoggerInstance.log( self.file_name_pop, str(self))
        LoggerInstance.log( self.file_name_pop, "#################################" )

    def logBest(self):
        if not self.logs_registered : 
            self.register_logs()
            self.logs_registered = True
        LoggerInstance.log( self.file_name_best, str(self.iteraiton) + ", " + str(self.best_pos) + ", " +  str(self.best_score))

    def get_next_to_check(self, score, cleaned):
        if self.iteraiton == self.max_iteration:
            return self.best_pos

        if self.numberOfPlayedGames < self.NUMBER_OF_PLAYED_GAMES:
            self.particles[self.index].curr_score += score * ROW_MULTIPLER + cleaned
            self.numberOfPlayedGames += 1
            return self.particles[self.index].pos_v
        self.numberOfPlayedGames = 0

        maxScore     = int(self.particles[self.index].curr_score / ROW_MULTIPLER)
        maxTetrimino = int((self.particles[self.index].curr_score - (maxScore*ROW_MULTIPLER)) / self.NUMBER_OF_PLAYED_GAMES)
        maxScore     = int(maxScore/self.NUMBER_OF_PLAYED_GAMES)
        newScore = maxScore * ROW_MULTIPLER + maxTetrimino

        self.particles[self.index].curr_score = newScore
        self.particles[self.index].update_best()

        if newScore > self.best_score: 
            self.best_score = newScore
            self.best_pos   = self.particles[self.index].pos_v
            self.logBest()
        
        self.particles[self.index].move(self.best_pos, self.ineria, self.congnitive_c, self.social_c)
        #print(str(self.index) + " " + str(self.particles[self.index]))

        self.index += 1
        if self.index == self.POPULATION_SIZE: 
            self.index = 0
            self.iteraiton += 1.0
            #if self.ineria < 0.001 : self.ineria = 0
            #else : self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 
            print( "Iteration ", self.iteraiton, " out of ", self.max_iteration)
            self.logInfo()

        Backup.save_pso(self.particles,  self.index, self.best_pos, self.best_score, self.iteraiton, self.dateTime, self.VECTOR_DIMENSIONS, self.spawnerId, self.congnitive_c, self.social_c, self.ineria)

        self.particles[self.index].curr_score = 0
        #print(str(self.index) + " " + str(self.particles[self.index]))
        return self.particles[self.index].pos_v
