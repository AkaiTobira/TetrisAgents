from os import name
from random import Random, uniform, randint
from math   import sqrt
from Libraries.vector import Vector
import time

from Libraries.Structures.logger import *
from Libraries.Structures.backupCreator import *
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME_EVO
from Libraries.Structures.best_saver import BestUnitsBackupSaver, BestUnitSaver
from Libraries.Structures.meansures import Meansures

class EvolutionAlgoritm:
	population             = []
	POPULATION_SIZE        = 50
	NEW_POPULATION_SIZE    = 35
	MUTATION_RATE          = 40
	NUMBER_OF_PLAYED_GAMES = 1
	EVOLUTION_VECTOR_DIMENSIONS = 4
	curenntly_played_game  = 0
	start                  = 0
	generation             = 0 
	unchecked_population   = []
	dateTime               = ""
	timer                  = 0
	contine_writing_logs   = False
	spawnerType            = 0
	TYPE = 1

	file_name_best =""
	file_name_avg  =""
	file_name_pop  =""

	def __init__(self, numberOfDimensions = 4, spawnerType = -1, numberOfGames = 8):

		self.population = []
		self.unchecked_population = []
		self.spawnerType = spawnerType

		self.EVOLUTION_VECTOR_DIMENSIONS = numberOfDimensions
		self.NUMBER_OF_PLAYED_GAMES      = numberOfGames
		Meansures.register_meansure("GenerationProcessing" + str(spawnerType))

		self.contine_writing_logs, self.population, self.unchecked_population, self.generation, self.dateTime = Backup.load_evolution(self.EVOLUTION_VECTOR_DIMENSIONS, self.POPULATION_SIZE, self.NUMBER_OF_PLAYED_GAMES, spawnerType, self.TYPE, self.MUTATION_RATE)

		if not self.contine_writing_logs:
			self.dateTime = DATE_TIME
			self.createPopulation()
		else:
			if len(self.unchecked_population) == 0: self.fit(False)

	def createPopulation(self):
		for i in range(self.POPULATION_SIZE):
			self.population.append([Vector( self.EVOLUTION_VECTOR_DIMENSIONS, unit=False ), 0])
			#for k in range(len(self.population[i][0].v)):
			#	self.population[i][0].v[k] = -abs(self.population[i][0].v[k])
		for i in range( self.POPULATION_SIZE):
			self.unchecked_population.append( [ i, self.population[i][0], 0 ] )

	def register_logs(self):
		self.file_name_best = "EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_G" + str(self.spawnerType)+ "_T" + str(self.TYPE) + "_M" + str(self.MUTATION_RATE) + "_best_change"
		self.file_name_avg  = "EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_G" + str(self.spawnerType)+ "_T" + str(self.TYPE) + "_M" + str(self.MUTATION_RATE) + "_avrg_change"
		self.file_name_pop   ="EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_G" + str(self.spawnerType)+ "_T" + str(self.TYPE) + "_M" + str(self.MUTATION_RATE) + "_populations"

		LoggerInstance.register_log( self.file_name_best, self.dateTime, "evo", continueSyle=self.contine_writing_logs)
		LoggerInstance.register_log( self.file_name_avg,  self.dateTime, "evo", continueSyle=self.contine_writing_logs)
		LoggerInstance.register_log( self.file_name_pop,  self.dateTime, "evo", continueSyle=self.contine_writing_logs)

	def add_score(self, score, cleaned):
		
		#end = time.time()
		self.unchecked_population[0][2] += score + cleaned 
		#self.moves.write( str(len( self.unchecked_population )) + "#" + str(self.unchecked_population[0][0]) + "#" + str(self.unchecked_population[0][1]) + "#" + str(self.unchecked_population[0][2]) + "#" + str((cleaned/5.0))[:5] + "%#" + str(end - self.start) + "\n" )
	#	print( len( self.unchecked_population ), self.unchecked_population[0][0], self.unchecked_population[0][1], self.unchecked_population[0][2], str((cleaned/MAX_NUMBER_PER_GAME_EVO * 100.0 ))[:6] + "%" )
		#self.start = end

	def get_next_active(self):
		self.curenntly_played_game += 1
		if self.curenntly_played_game < self.NUMBER_OF_PLAYED_GAMES:
			return self.unchecked_population[0][1].v
		
		#print( self.unchecked_population )

		self.replace_in_population()
		self.curenntly_played_game = 0
		if len(self.unchecked_population) == 0: self.fit()

		Backup.save_evolution(self)
		return self.unchecked_population[0][1].v

	def replace_in_population(self): 
		#index = self.unchecked_population[0][0]
		#if self.unchecked_population[0][2] >= self.population[index][1]: 
			#self.moves.write( "Replaced#"+ str(self.unchecked_population[0][2]) + "#" + str(self.population[index][1]) + "#" + str(index)  + "\n" )
			#print( "Replaced", self.unchecked_population[0][2], self.population[index][1], index, )
		#	self.population[index] = [ self.unchecked_population[0][1], self.unchecked_population[0][2] ]

		score = int(self.unchecked_population[0][2] / ROW_MULTIPLER)
		lines = self.unchecked_population[0][2] - (score*ROW_MULTIPLER)

		score = int(score/self.NUMBER_OF_PLAYED_GAMES)
		lines = int(lines/self.NUMBER_OF_PLAYED_GAMES)

		self.population.append([self.unchecked_population[0][1], score * ROW_MULTIPLER + lines])
		self.unchecked_population = self.unchecked_population[1:]

	def __str__(self):
		s = ""
		for i in self.population:
			s += "[" + str(i[0]) + ", " + str(i[1]) + "]\n"
		return s
    
	def select_best_two(self):
		return [ self.population[0], self.population[1]]

	def select_for_tournament(self):
		tournament = []
		for i in range(int(self.POPULATION_SIZE*0.1)):
			index = randint(0,self.POPULATION_SIZE-1)
			tournament.append( [index, self.population[index][0], self.population[index][1]] )

		f_best = tournament[0]
		s_best = tournament[0]
		for part in tournament:
			if part[2] >= f_best[2]:
				s_best = f_best.copy()
				f_best = part
	
		return [ f_best, s_best ]
	
	def select_for_rollette(self):
		max_value = 0
		for i in range(self.POPULATION_SIZE):
			max_value += int(self.population[i][1]/ROW_MULTIPLER)

		return [self.select_randomly(max_value), self.select_randomly(max_value)]

	def select_randomly(self, max_value):
		random_value = uniform(0, max_value)
		current_sum = 0
		for i in range(self.POPULATION_SIZE):
			current_sum += int(self.population[i][1]/ROW_MULTIPLER)
			if( random_value < current_sum ):
				return [i, self.population[i][0], self.population[i][1]]

	def select_randomly_ranked(self, population):
		random_value = uniform(0.0, 0.99)
		current_sum = 0
		s = 1.45
		pop_len = len(population)
		for i in range(pop_len):
			value = (2.0 - s)/float(pop_len) + float(2.0 * (pop_len-i-1) * (s-1.0))/float(pop_len *(pop_len-1))
			current_sum += value
			if(random_value < current_sum):
				return [i, population[i][0], population[i][1]]

	def select_for_ranking(self):
		ranked_population = self.population[0: int(0.3* self.POPULATION_SIZE)]
		return [self.select_randomly_ranked(ranked_population), self.select_randomly_ranked(ranked_population)]
			

	def crossover(self, parents):
		score1 = parents[0][2]/ROW_MULTIPLER
		score2 = parents[1][2]/ROW_MULTIPLER

		sume = score1 + score2

		new_one = Vector(self.EVOLUTION_VECTOR_DIMENSIONS,unit=True)
		if score1 < 0.01 or score2 < 0.01 : new_one = (parents[0][1] * ( 0.5 ) + parents[1][1] * (0.5))
		else : new_one = parents[0][1] * ( score1/sume ) + parents[1][1] * (score2/sume)
		
		new_one.mutate(self.MUTATION_RATE)
		return [new_one, 0]
			
	def sort(self):
		new_table = []
		buckets   = [ [], [], [], [], [], [], [], [], [], [] ] 

		multipler = 10**8

		for t in self.population:
			new_table.append( t )

		for i in range( 30 + 5 ):
			for element in new_table:
				buckets[int( element[1] * multipler / 10**i % 10 )].append(element)
			new_table = []

			for bucket in buckets:
				for element in bucket:
					new_table.append(element)

			buckets   = [ [], [], [], [], [], [], [], [], [], [] ] 

		mark = [ [],[]]
		for element in new_table:
			if element[1] < 0 : mark[0].append(element) 
			else: mark[1].append(element)

		new_table = mark[0] + mark[1]

		new_table.reverse()
		self.population = new_table
			
	def select_tepe(self):
		if self.TYPE == 0: return self.select_for_tournament()
		if self.TYPE == 1: return self.select_for_rollette()
		if self.TYPE == 2: return self.select_for_ranking()


	def fit(self, logInfoEnabled=True):
		#self.moves.write(" FIT CALLED " + "\n")
		new_generation = 0
		self.sort()

		self.population = self.population[:self.POPULATION_SIZE]
		self.unchecked_population = []

		while new_generation < self.NEW_POPULATION_SIZE - int(0.05*self.POPULATION_SIZE):
			t = self.select_tepe()
			temp = self.crossover(t)
			self.unchecked_population.append([t[0][0], temp[0], temp[1]])
			temp = self.crossover(t)
			self.unchecked_population.append([t[1][0], temp[0], temp[1]])
			new_generation += 2
#			new_generation.append(self.crossover(t))
#		self.population =  self.population[0:(self.POPULATION_SIZE - int(0.3*self.POPULATION_SIZE))] + new_generation
		
		for i in range(int(0.1*self.POPULATION_SIZE)):
			self.unchecked_population.append([ self.POPULATION_SIZE-i-1, Vector(self.EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

		self.unchecked_population = self.unchecked_population[:self.NEW_POPULATION_SIZE]

		if logInfoEnabled:
			self.register_logs()
			self.logInfo()
			self.generation += 1
			print( "Generation " + str(self.generation))


	def logInfo(self):
		name2 = "Evolution" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_G" + str(self.spawnerType) + "_D" + str(self.NUMBER_OF_PLAYED_GAMES) + "_" + str(MAX_NUMBER_PER_GAME_EVO)
		if self.TYPE != 0: name2 += "_T" + str(self.TYPE)
		name2 += "_M" + str(self.MUTATION_RATE)

		BestUnitsBackupSaver.saveScore(name2, self.population[0][0], self.population[0][1] )

		avrg_lines      = 0.0
		avrg_tetriminos = 0.0
		for i in range( self.POPULATION_SIZE ):
			lines = int(self.population[i][1] / ROW_MULTIPLER)
			avrg_lines      += lines
			avrg_tetriminos += self.population[i][1] - (lines*ROW_MULTIPLER)

		avrg_lines /= self.POPULATION_SIZE
		avrg_tetriminos /= self.POPULATION_SIZE

		print(str(self.population[0][1]) + " Avg_Lines :" + str(avrg_lines) + " Avg_Tetriminos :" + str(avrg_tetriminos))

		LoggerInstance.log( self.file_name_best, str(self.generation) + ", " + str(self.population[0][1]) + ", " + str(self.population[0][0]) )
		LoggerInstance.log( self.file_name_avg, str(self.generation) + ", " + str(avrg_lines) + ", " + str(avrg_tetriminos) + ", " + str(Meansures.lap_meansure("GenerationProcessing" + str(self.spawnerType))))
		LoggerInstance.log( self.file_name_pop, str(self))
		LoggerInstance.log( self.file_name_pop, "#################################" )



	def get_fittest(self):
		f_best = self.population[self.POPULATION_SIZE-1]
		s_best = self.population[self.POPULATION_SIZE-1]
		
		for part in self.population:
			if part[1] >= f_best[1]:
				s_best = f_best
				f_best = part
				
		return [ f_best, s_best ]
