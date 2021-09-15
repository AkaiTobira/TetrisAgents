

import math
from random import Random, random, uniform, randint, seed
from math   import sqrt
from Libraries.vector import Vector
import time

from Libraries.Structures.logger import *
from Libraries.Structures.backupCreator import *
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME_EVO
from Libraries.Structures.best_saver import BestUnitsBackupSaver, BestUnitSaver
from Libraries.Structures.meansures import Meansures
from Libraries.Structures.settings import *

SCORE_INDEX  = 1
VECTOR_INDEX = 0

def bucket_sort(table_to_sort):
    new_table = []
    buckets   = [ [], [], [], [], [], [], [], [], [], [] ] 

    multipler = 10**8

    for t in table_to_sort:
        new_table.append( t )

    for i in range( 30 + 5 ):
        for element in new_table:
            buckets[int( element[1] * multipler / 10**i % 10 )].append(element)
        new_table = []

        for bucket in buckets:
            for element in bucket:
                new_table.append(element)

        buckets   = [ [], [], [], [], [], [], [], [], [], [] ] 

    mark = [[],[]]
    for element in new_table:
        if element[1] < 0 : mark[0].append(element) 
        else: mark[1].append(element)

    new_table = mark[0] + mark[1]
    new_table.reverse()

    return new_table


class EvolutionAlgoritm2:
    population             = []
    parents                = []
    prev_population        = []
    unchecked_population   = []

    curenntly_played_game  = 0
    generation             = 0 
    best_found             = []
    dateTime               = ""

    contine_writing_logs   = False
    avrg_tetriminos         = [0, 0]

    NAME = ""

    file_name_best =""
    file_name_avg  =""
    file_name_pop  =""

    def construct_save_name(self):
        _name = "EVO" + str(PARAMS.HEURYSTIC_AMOUNT)
        _name += "_PSIZE" + str(PARAMS.POPULATION_SIZE)
        _name += "_GEN" + str(PARAMS.GENERATOR)
        _name += "_MRATE" + str(PARAMS.MUTATION_RATE)
        _name += "_TLimit" + str(PARAMS.MAX_POINTS)
        _name += "_PER" + str(PARAMS.NUMBER_OF_GAMES)
        _name += "_ELIT" + str(PARAMS.ELITARY_SELECT)
        _name += "_REPType" + str(PARAMS.REPLACE_IN_POPULATION_TYPE)
        _name += "_SELType" + str(PARAMS.SELECTION_TYPE)
        _name += "_PARSEL"  + str(PARAMS.PARENTS_SELECT)
        _name += "_LNI" + str(PARAMS.LIMIT_NOT_IMPROVE)
        _name += "_SEL_LIM" + str(PARAMS.SELECTION_LIMIT)
        _name += "_SEL_PAR" + str(PARAMS.RANKING_RATE)
        return _name

    def __init__(self):
        Meansures.register_meansure("GenerationProcessing" + str(PARAMS.GENERATOR))

        self.population           = []
        self.unchecked_population = []

        self.NAME = self.construct_save_name()

        self.contine_writing_logs = Backup.load_evolution(self)

        if not self.contine_writing_logs:
            self.dateTime = DATE_TIME
            self.createPopulation()

        self.register_logs()
        if len(self.unchecked_population) == 0: self.fit()

    def createPopulation(self):
        seed(COMMON_SEED)
        for i in range(PARAMS.POPULATION_SIZE):
            self.population.append([Vector( PARAMS.HEURYSTIC_AMOUNT, unit=False ), 0])

            #dimension_i = 0
            #for j in range(len(HEURYSTIC_LIST)):
            #    if dimension_i >= self.EVOLUTION_VECTOR_DIMENSIONS: break
            #    if not HEURYSTIC_LIST[j][0]: continue
            #    self.population[i][0].v[dimension_i] = abs(self.population[i][0].v[dimension_i]) * HEURYSTIC_LIST[j][1]
            #    dimension_i += 1


        for i in range(PARAMS.POPULATION_SIZE):
            self.unchecked_population.append( [self.population[i][VECTOR_INDEX], 0] )
        self.population = []
        seed(COMMON_SEED)

    def register_logs(self):
        self.file_name_best = self.NAME + "_best_change"
        self.file_name_avg  = self.NAME + "_avrg_change"
        self.file_name_pop  = self.NAME + "_populations"

        LoggerInstance.register_log( self.file_name_best, self.dateTime, "evo", continueSyle=self.contine_writing_logs)
        LoggerInstance.register_log( self.file_name_avg,  self.dateTime, "evo", continueSyle=self.contine_writing_logs)
        LoggerInstance.register_log( self.file_name_pop,  self.dateTime, "evo", continueSyle=self.contine_writing_logs)

    def add_score(self, score, cleaned):
        if len(self.unchecked_population) == 0: return
        #end = time.time()
        self.unchecked_population[0][SCORE_INDEX] += score + cleaned 
        #self.moves.write( str(len( self.unchecked_population )) + "#" + str(self.unchecked_population[0][0]) + "#" + str(self.unchecked_population[0][1]) + "#" + str(self.unchecked_population[0][2]) + "#" + str((cleaned/5.0))[:5] + "%#" + str(end - self.start) + "\n" )
    #    print( len( self.unchecked_population ), self.unchecked_population[0][0], self.unchecked_population[0][1], self.unchecked_population[0][2], str((cleaned/MAX_NUMBER_PER_GAME_EVO * 100.0 ))[:6] + "%" )
        #self.start = end

    def get_first_to_check(self):
        if self.over_condition(): return BestUnitsBackupSaver.getLastBest(self.NAME)
        return self.unchecked_population[0][VECTOR_INDEX]

    def get_next_active(self):
        self.curenntly_played_game += 1
        if self.curenntly_played_game < PARAMS.NUMBER_OF_GAMES:
            if len(self.unchecked_population) == 0: return self.best_found[0]
            return self.unchecked_population[0][VECTOR_INDEX]
        
        #print( self.unchecked_population )

        self.replace_in_population()
        last_add = self.population[len(self.population)-1]

        BestUnitsBackupSaver.saveScore(self.NAME, last_add[VECTOR_INDEX], last_add[SCORE_INDEX], self.generation)
        self.best_found = [BestUnitsBackupSaver.getLastBest(self.NAME), BestUnitsBackupSaver.getLastBestScore(self.NAME) ]

        self.curenntly_played_game = 0
        if len(self.unchecked_population) == 0: self.fit()
        if len(self.unchecked_population) == 0: return self.best_found[0]

        Backup.save_evolution(self)
        return self.unchecked_population[0][VECTOR_INDEX]

    def replace_in_population(self): 
        if len(self.unchecked_population) == 0: return

        score = int(self.unchecked_population[0][SCORE_INDEX] / ROW_MULTIPLER)
        lines = self.unchecked_population[0][SCORE_INDEX] - (score*ROW_MULTIPLER)

        score = int(score/PARAMS.NUMBER_OF_GAMES)
        lines = int(lines/PARAMS.NUMBER_OF_GAMES)

        self.population.append([self.unchecked_population[0][VECTOR_INDEX], score * ROW_MULTIPLER + lines])
        self.unchecked_population = self.unchecked_population[1:]

    def __str__(self):
        s = ""
        for i in self.population:
            s += "[" + str(i[VECTOR_INDEX]) + ", " + str(i[SCORE_INDEX]) + "]\n"
        return s

    def select_for_elit_tournament(self):
        tournament = []
        for i in range(PARAMS.SELECTION_LIMIT):
            index = randint(0,len(self.population)-1)
            tournament.append( [self.population[index][VECTOR_INDEX], self.population[index][SCORE_INDEX]] )

        f_best = tournament[0]
        for part in tournament:
            if part[SCORE_INDEX] >= f_best[SCORE_INDEX]:
                f_best = part
    
        return f_best


    def crossover(self, parent1, parent2):
        score1 = parent1[SCORE_INDEX]/ROW_MULTIPLER
        score2 = parent2[SCORE_INDEX]/ROW_MULTIPLER

        sume = score1 + score2

        new_one = Vector(PARAMS.HEURYSTIC_AMOUNT,unit=True)
        if score1 < 0.01 or score2 < 0.01 : new_one = (parent1[VECTOR_INDEX] * ( 0.5 ) + parent2[VECTOR_INDEX] * (0.5))
        else : new_one = parent1[VECTOR_INDEX] * ( score1/sume ) + parent2[VECTOR_INDEX] * (score2/sume)
        
        return new_one

    def select_tepe(self):
        if PARAMS.NUMBER_OF_GAMES == 0: return self.select_for_tournament()
        if self.TYPE == 1: return self.select_for_rollette()
        if self.TYPE == 2: return self.select_for_ranking()

    def repopulate_70_elite(self): 
        self.population = self.population[:self.POPULATION_SIZE]
        self.unchecked_population = []

        new_generation = 0
        while new_generation < self.NEW_POPULATION_SIZE - int(0.05*len(self.population)):
            t = self.select_tepe()
            temp = self.crossover(t)
            self.unchecked_population.append([t[0][0], temp[0], temp[1]])
            temp = self.crossover(t)
            self.unchecked_population.append([t[1][0], temp[0], temp[1]])
            new_generation += 2

        self.unchecked_population = self.unchecked_population[:self.NEW_POPULATION_SIZE]

    def repopulate_all(self):
        self.population = self.population[:len(self.population)]
        self.unchecked_population = []

        new_generation = 0
        while new_generation < self.NEW_POPULATION_SIZE - int(0.05*len(self.population)):
            t = self.select_tepe()
            temp = self.crossover(t)
            self.unchecked_population.append([t[0][0], temp[0], temp[1]])
            new_generation += 1

        for i in range(int(0.1*len(self.population))):
            self.unchecked_population.append([ len(self.population)-i-1, Vector(self.EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

        self.unchecked_population = self.unchecked_population[:self.NEW_POPULATION_SIZE]
        self.population = []

    def repopulate_random(self):
        self.population = self.population[:len(self.population)]
        self.unchecked_population = []

        new_generation = 0
        while new_generation < self.NEW_POPULATION_SIZE - int(0.05*len(self.population)):
            t = self.select_tepe()
            temp = self.crossover(t)
            self.unchecked_population.append([t[0][0], temp[0], temp[1]])
            new_generation += 1

        for i in range(int(0.1*len(self.population))):
            self.unchecked_population.append([ len(self.population)-i-1, Vector(self.EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

        self.unchecked_population = self.unchecked_population[:self.NEW_POPULATION_SIZE]

        while len(self.population) > self.NEW_POPULATION_SIZE:
            index = randint(0,len(self.population)-1)
            self.population = self.population[:index] + self.population[index+1:]

    def repopulate_by_coomon(self):
        self.population = self.population[:len(self.population)]
        self.unchecked_population = []

        new_generation = 0
        while new_generation < self.NEW_POPULATION_SIZE - int(0.05*len(self.population)):
            t = self.select_tepe()
            temp = self.crossover(t)
            self.unchecked_population.append([t[0][0], temp[0], temp[1]])
            new_generation += 1

        for i in range(int(0.1*len(self.population))):
            self.unchecked_population.append([ len(self.population)-i-1, Vector(self.EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

        self.unchecked_population = self.unchecked_population[:self.NEW_POPULATION_SIZE]

        for i in range(len(self.unchecked_population)):
            vectorLen = self.unchecked_population[i][1].len()
            currLen = 999
            closestIndex = -1
            for j in range(10):
                index = randint(0,len(self.population)-1)
                if currLen > math.fabs(self.population[j][0].len() - vectorLen):
                    closestIndex = index
                    currLen = math.fabs(self.population[j][0].len() - vectorLen)
            self.population = self.population[:closestIndex] + self.population[closestIndex+1:]

    def select_for_rollette(self):
        max_value = 0
        for i in range(len(self.population)):
            max_value += int(self.population[i][SCORE_INDEX]/ROW_MULTIPLER) + 1

        return self.select_randomly(max_value)

    def select_randomly(self, max_value):
        random_value = uniform(0, max_value)
        current_sum = 0
        for i in range(len(self.population)):
            current_sum += int(self.population[i][SCORE_INDEX]/ROW_MULTIPLER) + 1
            if( random_value < current_sum ):
                return [self.population[i][VECTOR_INDEX], self.population[i][SCORE_INDEX]]

    def select_randomly_ranked(self, population):
        random_value = uniform(0.0, 0.99)
        current_sum = 0
        s = PARAMS.RANKING_RATE
        pop_len = len(population)
        for i in range(pop_len):
            value = (2.0 - s)/float(pop_len) + float(2.0 * (pop_len-i-1) * (s-1.0))/float(pop_len *(pop_len-1))
            current_sum += value
            if(random_value < current_sum):
                return [population[i][VECTOR_INDEX], population[i][SCORE_INDEX]]

    def select_for_ranking(self):
        ranked_population = bucket_sort(self.population)
        ranked_population = ranked_population[0: PARAMS.SELECTION_LIMIT]
        return self.select_randomly_ranked(ranked_population)

    def get_parents(self):
        if PARAMS.SELECTION_TYPE == 0: return self.select_for_rollette()
        if PARAMS.SELECTION_TYPE == 1: return self.select_for_ranking()
        if PARAMS.SELECTION_TYPE == 2: return self.select_for_elit_tournament()
    #    if self.FIT_TYPE == 1: self.repopulate_all()
    #    if self.FIT_TYPE == 2: self.repopulate_random()
    #    if self.FIT_TYPE == 3: self.repopulate_by_coomon()

    def replace_population_whole(self):
        self.prev_population = bucket_sort(self.prev_population)
        self.population += self.prev_population[:PARAMS.ELITARY_SELECT]

    def replace_population_elit(self):
        self.prev_population += self.population
        self.prev_population = bucket_sort(self.prev_population)
        self.population = self.prev_population[:PARAMS.POPULATION_SIZE]

    def replace_population(self):
        if PARAMS.REPLACE_IN_POPULATION_TYPE == 0: self.replace_population_whole() 
        if PARAMS.REPLACE_IN_POPULATION_TYPE == 1: self.replace_population_elit() 

    def over_condition(self):
        if not BestUnitsBackupSaver.hasScoreFor(self.NAME) : return False

        score = BestUnitsBackupSaver.getLastBestScore(self.NAME)
        tetrimino = (score - (int(score / ROW_MULTIPLER) * ROW_MULTIPLER))
        if tetrimino > PARAMS.MAX_POINTS: 
            PARAMS.LEARNING_STATUS = 100
            return True

        if self.avrg_tetriminos[1] > PARAMS.LIMIT_NOT_IMPROVE: 
            print("Not improved by" + str(PARAMS.LIMIT_NOT_IMPROVE) + " : Broking")
            PARAMS.LEARNING_STATUS = int(tetrimino/PARAMS.MAX_POINTS * 100)
            return True

    def fit(self):
        if self.over_condition():
            print("Complete : ",self.NAME)
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_m)
            pygame.event.post(event)
            return

        seed(COMMON_SEED + self.generation)
        self.repopulate()

    def repopulate(self):
        self.unchecked_population = []

        if self.prev_population != None: self.replace_population()

        self.logInfo()
        self.generation += 1

        self.parents = []
        for i in range( int(PARAMS.PARENTS_SELECT) ):
            self.parents.append(self.get_parents())

        mutated = 0
        crossed = 0

        for parent in self.parents:
            if(int(uniform(0, 2)) == 0):
                parent2 = self.parents[ int(uniform(0, len(self.parents))) ]
                child = self.crossover(parent, parent2)
                self.unchecked_population.append([child, 0])
                crossed += 1
            elif uniform(0,100) < PARAMS.MUTATION_RATE:
                child = Vector(PARAMS.HEURYSTIC_AMOUNT)
                for i in range(0,PARAMS.HEURYSTIC_AMOUNT):
                    child[i] = parent[VECTOR_INDEX][i]
                child.mutate()
                self.unchecked_population.append([child, 0])
                mutated += 1

        print( "Generation " + str(self.generation) + " Mutated :" + str(mutated) + " Crossed :" + str(crossed))
        self.prev_population = self.population
        self.population = []

    def get_second_parent(self):
        parents_beta = []
        while(len(parents_beta) < 0.3 * self.parents):
            parents_beta.append[self.parents[int(uniform(0, len(self.parents)))]]
        parents_beta = bucket_sort(parents_beta)
        return parents_beta[0]


    def get_fittest(self):
        f_best = self.population[len(self.population)-1]
        s_best = self.population[len(self.population)-1]
        
        for part in self.population:
            if part[1] >= f_best[1]:
                s_best = f_best
                f_best = part
                
        return [ f_best, s_best ]

    def logInfo(self):
        avrg_lines      = 0.0
        avrg_tetriminos = 0.0
        for i in range( len(self.population) ):
            lines = int(self.population[i][SCORE_INDEX] / ROW_MULTIPLER)
            avrg_lines      += lines
            avrg_tetriminos += self.population[i][SCORE_INDEX] - (lines*ROW_MULTIPLER)

        avrg_lines /= len(self.population)
        avrg_tetriminos /= len(self.population)

        if(avrg_tetriminos > self.avrg_tetriminos[0]):
            self.avrg_tetriminos[1] = 0
            self.avrg_tetriminos[0] = avrg_tetriminos
        else: self.avrg_tetriminos[1] += 1

        print(str(self.get_fittest()[0][SCORE_INDEX]) + " Avg_Lines :" + str(avrg_lines) + " Avg_Tetriminos :" + str(avrg_tetriminos))

        LoggerInstance.log( self.file_name_best, str(self.generation) + ", " + str(self.population[0][SCORE_INDEX]) + ", " + str(self.population[0][VECTOR_INDEX]) )
        LoggerInstance.log( self.file_name_avg, str(self.generation) + ", " + str(avrg_lines) + ", " + str(avrg_tetriminos) + ", " + str(Meansures.lap_meansure("GenerationProcessing" + str(PARAMS.GENERATOR))))
        LoggerInstance.log( self.file_name_pop, str(self))
        LoggerInstance.log( self.file_name_pop, "#################################" )

