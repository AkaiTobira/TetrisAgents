from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME, ROW_MULTIPLER
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

    POPULATION_SIZE = 0
    index           = 0
    iteraiton       = 0
    max_iteration   = 0.0
    numberOfPlayedGames = 0

    ineria     = 0.9

    file_name_best = ""
    file_name_avg  = ""
    file_name_pop  = ""

    VECTOR_DIMENSIONS = 4

    logs_registered = False
    dateTime        = ""

    def __init__(self, vector_dimensions, population_size,  numberOfIteration=500):
        self.logs_registered = False
        self.VECTOR_DIMENSIONS = vector_dimensions
        self.POPULATION_SIZE = population_size
        self.max_iteration   = numberOfIteration
        self.particles = []
        Meansures.register_meansure("GenerationProcessingPSO")

        self.continueSyle, self.particles, self.iteraiton, self.dateTime, self.index, self.best_pos, self.best_score = Backup.load_pso( self.VECTOR_DIMENSIONS, self.POPULATION_SIZE)

        if not self.continueSyle:
            self.dateTime = DATE_TIME
            self.best_pos = Vector(vector_dimensions)
            for _ in range( self.POPULATION_SIZE ): 
                self.particles.append( Particle(vector_dimensions) )
            self.index = 0

        self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 

    def __str__(self):
        s = ""
        for i in range( len(self.particles) ):
            s += "["+ str(i) + str( self.particles[i] )  + "]\n"
        return s

    def register_logs(self):
        self.file_name_best = "PSO" + str(self.VECTOR_DIMENSIONS) + "_best_change"
        self.file_name_avg  = "PSO" + str(self.VECTOR_DIMENSIONS) + "_avrg_change"
        self.file_name_pop   ="PSO" + str(self.VECTOR_DIMENSIONS) + "_populations"
        LoggerInstance.register_log( self.file_name_best, self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_avg,  self.dateTime, "pso", continueSyle=self.continueSyle)
        LoggerInstance.register_log( self.file_name_pop,  self.dateTime, "pso", continueSyle=self.continueSyle)

    def logInfo(self):
        if not self.logs_registered : 
            self.register_logs()
            self.logs_registered = True

        BestUnitsBackupSaver.saveScore("PSO" + str(self.VECTOR_DIMENSIONS), self.best_pos, self.best_score )

        avrg = 0.0
        for i in range( self.POPULATION_SIZE ):
            avrg += self.particles[i].curr_score
        avrg /= self.POPULATION_SIZE

        LoggerInstance.log( self.file_name_avg, str(self.iteraiton) + ", " + str(avrg) + ", " + str(Meansures.lap_meansure("GenerationProcessingPSO")))
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

        print( str(self.index), str(self.particles[self.index].pos_v), str(score), str((cleaned/MAX_NUMBER_PER_GAME * 100.0 ))[:6] + "%" )

        if self.numberOfPlayedGames < 4:
            self.numberOfPlayedGames += 1
            if self.numberOfPlayedGames == 1:
                self.particles[self.index].curr_score = 0
            self.particles[self.index].curr_score += score * ROW_MULTIPLER + cleaned
            return self.particles[self.index].pos_v
        self.numberOfPlayedGames = 0

        if self.particles[self.index].curr_score > self.particles[self.index].best_score: 
            self.particles[self.index].update_best(self.particles[self.index].curr_score)
        if self.particles[self.index].curr_score > self.best_score: 
            self.logBest()
            self.best_score = self.particles[self.index].curr_score
            self.best_pos   = self.particles[self.index].best_pos
        
        self.particles[self.index].move(self.best_pos, self.ineria, 1.5,1)

        self.index += 1
        if self.index == self.POPULATION_SIZE: 
            self.index = 0
            self.iteraiton += 1.0
            if self.ineria < 0.001 : self.ineria = 0
            else : self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 
            print( "Iteration ", self.iteraiton, " out of ", self.max_iteration)
            self.logInfo()

        Backup.save_pso(self.particles, self.index, self.best_pos, self.best_score, self.iteraiton, self.dateTime, self.VECTOR_DIMENSIONS)

        return self.particles[self.index].pos_v
