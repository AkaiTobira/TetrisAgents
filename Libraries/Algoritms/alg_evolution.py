from random import uniform, randint
from math   import sqrt
from Libraries.vector import Vector
import time
from Libraries.consts import DATE_TIME

EVOLUTION_VECTOR_DIMENSIONS = 4

class EvolutionAlgoritm:
	population             = []
	POPULATION_SIZE        = 50
	MUTATION_RATE          = 30
	NUMBER_OF_PLAYED_GAMES = 5
	curenntly_played_game  = 0
	dumps                  = None
	moves                  = None
	start                  = 0
	unchecked_population = []

	def __init__(self):
		self.dumps = open("logs/evo/EVO_GEN_" + DATE_TIME, "w")
		self.moves = open("logs/evo/EVO_MOV_" + DATE_TIME, "w")

		self.population = []
		self.unchecked_population = []

		for i in range(self.POPULATION_SIZE):
			self.population.append([Vector( EVOLUTION_VECTOR_DIMENSIONS, unit=True ), 0])

		for i in range( self.POPULATION_SIZE):
			self.unchecked_population.append( [ i, self.population[i][0], 0 ] )

	def add_score(self, score, cleaned):
		
		end = time.time()
		self.unchecked_population[0][2] += score
		self.moves.write( str(len( self.unchecked_population )) + "#" + str(self.unchecked_population[0][0]) + "#" + str(self.unchecked_population[0][1]) + "#" + str(self.unchecked_population[0][2]) + "#" + str((cleaned/5.0))[:5] + "%#" + str(end - self.start) + "\n" )
		print( len( self.unchecked_population ), self.unchecked_population[0][0], self.unchecked_population[0][1], self.unchecked_population[0][2], str((cleaned/5.0))[:5] + "%" )
		self.start = end

	def get_next_active(self):
		self.curenntly_played_game += 1
		if self.curenntly_played_game < self.NUMBER_OF_PLAYED_GAMES:
			return self.unchecked_population[0][1].v
		
		self.replace_in_population()
		self.curenntly_played_game = 0
		if len(self.unchecked_population) == 0: self.fit() 

		print( self.unchecked_population )

		return self.unchecked_population[0][1].v

	def replace_in_population(self): 
		index = self.unchecked_population[0][0]
		if self.unchecked_population[0][2] >= self.population[index][1]: 
			self.moves.write( "Replaced#"+ str(self.unchecked_population[0][2]) + "#" + str(self.population[index][1]) + "#" + str(index)  + "\n" )
			print( "Replaced", self.unchecked_population[0][2], self.population[index][1], index, )
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

		new_one = Vector(EVOLUTION_VECTOR_DIMENSIONS,unit=True)

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
			
	def fit(self):
		self.moves.write(" FIT CALLED " + "\n")
		new_generation = 0
		self.sort()

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
			self.unchecked_population.append([ self.POPULATION_SIZE-i-1, Vector(EVOLUTION_VECTOR_DIMENSIONS, unit=True), 0 ] )

		self.dumps.write("############################################################################################################################################\n")
		self.dumps.write(str(self))
				
	def get_fittest(self):
		f_best = self.population[self.POPULATION_SIZE-1]
		s_best = self.population[self.POPULATION_SIZE-1]
		
		for part in self.population:
			if part[1] >= f_best[1]:
				s_best = f_best
				f_best = part
				
		return [ f_best, s_best ]
