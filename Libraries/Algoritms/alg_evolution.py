from random import uniform, randint
from math   import sqrt
from Libraries.vector import Vector
import time

from Libraries.Structures.logger import *
from Libraries.Structures.backupCreator import *
from Libraries.consts import DATE_TIME, MAX_NUMBER_PER_GAME
from Libraries.Structures.best_saver import instance, BestUnitSaver

class EvolutionAlgoritm:
	population             = []
	POPULATION_SIZE        = 100
	MUTATION_RATE          = 15
	NUMBER_OF_PLAYED_GAMES = 5
	EVOLUTION_VECTOR_DIMENSIONS = 4
	curenntly_played_game  = 0
	start                  = 0
	generation             = 0 
	unchecked_population   = []
	dateTime               = ""

	file_name_best =""
	file_name_avg  =""
	file_name_pop  =""

	def __init__(self, numberOfDimensions = 4):

		self.population = []
		self.unchecked_population = []

		self.EVOLUTION_VECTOR_DIMENSIONS = numberOfDimensions

		#lastbest = instance.getLastBest("Evolution" + str(EVOLUTION_VECTOR_DIMENSIONS))
		#unit = Vector(EVOLUTION_VECTOR_DIMENSIONS, unit = True)
		#unit.v = lastbest[0]

		#self.population.append( [unit, 0])

		style, self.population, self.generation, self.dateTime = Backup.load_evolution(self.EVOLUTION_VECTOR_DIMENSIONS, self.POPULATION_SIZE, self.NUMBER_OF_PLAYED_GAMES)

		if not style:
			self.dateTime = DATE_TIME
			self.createPopulation()
		else:
			self.fit(False)

		self.register_logs(self.dateTime, style)

	def createPopulation(self):
		for i in range(self.POPULATION_SIZE):
			self.population.append([Vector( self.EVOLUTION_VECTOR_DIMENSIONS, unit=True ), 0])
		for i in range( self.POPULATION_SIZE):
			self.unchecked_population.append( [ i, self.population[i][0], 0 ] )

	def register_logs(self, dateTime, style):
		self.file_name_best = "EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_best_change"
		self.file_name_avg  = "EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_avrg_change"
		self.file_name_pop   ="EVO" + str(self.EVOLUTION_VECTOR_DIMENSIONS) + "_populations"

		LoggerInstance.register_log( self.file_name_best, dateTime, continueSyle=style)
		LoggerInstance.register_log( self.file_name_avg,  dateTime, continueSyle=style)
		LoggerInstance.register_log( self.file_name_pop,  dateTime, continueSyle=style)

	def add_score(self, score, cleaned):
		
		#end = time.time()
		self.unchecked_population[0][2] +=  score + cleaned 
		#self.moves.write( str(len( self.unchecked_population )) + "#" + str(self.unchecked_population[0][0]) + "#" + str(self.unchecked_population[0][1]) + "#" + str(self.unchecked_population[0][2]) + "#" + str((cleaned/5.0))[:5] + "%#" + str(end - self.start) + "\n" )
		print( len( self.unchecked_population ), self.unchecked_population[0][0], self.unchecked_population[0][1], self.unchecked_population[0][2], str((cleaned/MAX_NUMBER_PER_GAME * 100.0 ))[:6] + "%" )
		#self.start = end

	def get_next_active(self):
		self.curenntly_played_game += 1
		if self.curenntly_played_game < self.NUMBER_OF_PLAYED_GAMES:
			return self.unchecked_population[0][1].v
		
		#print( self.unchecked_population )

		self.replace_in_population()
		self.curenntly_played_game = 0
		if len(self.unchecked_population) == 0: self.fit() 

		return self.unchecked_population[0][1].v

	def replace_in_population(self): 
		
		#self.population.append([self.unchecked_population[0][1], self.unchecked_population[0][2]])
		
		index = self.unchecked_population[0][0]
		if self.unchecked_population[0][2] >= self.population[index][1]: 
			#self.moves.write( "Replaced#"+ str(self.unchecked_population[0][2]) + "#" + str(self.population[index][1]) + "#" + str(index)  + "\n" )
			#print( "Replaced", self.unchecked_population[0][2], self.population[index][1], index, )
			self.population[index] = [ self.unchecked_population[0][1], self.unchecked_population[0][2] ]
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
	
	def crossover(self, parents):
		sume = parents[0][2] + parents[1][2]

		new_one = Vector(self.EVOLUTION_VECTOR_DIMENSIONS,unit=True)

		if sume == 0 : new_one = (parents[0][1] * ( 0.5 ) + parents[1][1] * (0.5))
		else : new_one = parents[0][1] * ( parents[0][2] / sume ) + parents[1][1] * (parents[1][2]/sume)
		
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
			
	def fit(self, logInfoEnabled=True):
		#self.moves.write(" FIT CALLED " + "\n")
		new_generation = 0
		self.sort()

		self.population = self.population[:self.POPULATION_SIZE]

		while new_generation < int(0.3*self.POPULATION_SIZE) :
			t = self.select_for_tournament()
			temp = self.crossover(t)
			self.unchecked_population.append([t[0][0], temp[0], temp[1]])
			temp = self.crossover(t)
			self.unchecked_population.append([t[1][0], temp[0], temp[1]])
			new_generation += 2
#			new_generation.append(self.crossover(t))
#		self.population =  self.population[0:(self.POPULATION_SIZE - int(0.3*self.POPULATION_SIZE))] + new_generation
		
		for i in range(int(0.05*self.POPULATION_SIZE)):
			self.unchecked_population.append([ self.POPULATION_SIZE-i-1, Vector(self.EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

		if logInfoEnabled: 
			self.logInfo()
			Backup.save_evolution( self.population, self.generation, self.dateTime, self.MUTATION_RATE, self.NUMBER_OF_PLAYED_GAMES, self.EVOLUTION_VECTOR_DIMENSIONS)

			self.generation += 1
			print( "Generation " + str(self.generation))



	def logInfo(self):
		instance.saveScore("Evolution" + str(self.EVOLUTION_VECTOR_DIMENSIONS), self.population[0][0], self.population[0][1] )

		avrg = 0.0
		for i in range( self.POPULATION_SIZE ):
			avrg += self.population[i][1]
		avrg /= self.POPULATION_SIZE

		LoggerInstance.log( self.file_name_best, str(self.generation) + ", " + str(self.population[0][1]) + ", " + str(self.population[0][0]) )
		LoggerInstance.log( self.file_name_avg, str(self.generation) + ", " + str(avrg))
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
