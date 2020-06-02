from neural_network import Matrix, NeuralNetwork, NeuralNetworkLayer, layer_crossover
from random import uniform, randint
from math   import sqrt
from consts import DATE_TIME
import time

class NeuralEvolution:
    population          = []
    POPULATION_SIZE = 1
    MUTATION_RATE   = 0.01
    NUMBER_OF_PLAYED_GAMES = 1
    curenntly_played_game  = 0
    dumps           = None
    moves           = None
    start           = 0
    unchecked_population = []
    generation      = 0
    def __init__(self):
        self.dumps = open("logs/nevo/NEVO_GEN_" + DATE_TIME, "w")
        self.moves = open("logs/nevo/NEVO_MOV_" + DATE_TIME, "w")

        self.population = []
        self.unchecked_population = []

#        for i in range(self.POPULATION_SIZE):
 #           self.population.append([NeuralNetwork( 227, 3, 128, 32), 0])
  #          print( i, " Network done")

   #     for i in range( self.POPULATION_SIZE):
    #        self.unchecked_population.append( [ i, self.population[i][0], 0 ] )

    def add_score(self, score, cleaned):
        
        end = time.time()
        self.unchecked_population[0][2] += score
        self.moves.write( str(len( self.unchecked_population )) + "#" + str(self.unchecked_population[0][0]) + "#" + str(self.unchecked_population[0][1]) + "#" + str(self.unchecked_population[0][2]) + "#" + str((cleaned/5.0))[:5] + "%#" + str(end - self.start) + "\n" )
        print( len( self.unchecked_population ), self.unchecked_population[0][0], self.unchecked_population[0][1], self.unchecked_population[0][2], str((cleaned/5.0))[:5] + "%" )
        self.start = end

    def get_next_active(self):
        self.curenntly_played_game += 1
        if self.curenntly_played_game < self.NUMBER_OF_PLAYED_GAMES:
            return self.unchecked_population[0][1]
        
        self.replace_in_population()
        self.curenntly_played_game = 0
        if len(self.unchecked_population) == 0: self.fit() 
        return self.unchecked_population[0][1]

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
        next_generation = NeuralNetwork( 227, 3, 128, 32)

        p_copy = [ parents[0][1].copy(), parents[1][1].copy() ]

        for layer_i in range(len(next_generation.layers)):
            next_generation.layers[layer_i] = layer_crossover( p_copy[0].layers[layer_i], p_copy[1].layers[layer_i] )
    
        next_generation.mutate(self.MUTATION_RATE)
        return next_generation
            
    def sort(self):
        new_table = []
        buckets   = [ [], [], [], [], [], [], [], [], [], [] ] 

        multipler = 10**8

        for t in self.population:
            new_table.append( t )

        for i in range( 8 + 5 ):
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
        print(" FIT CALLED ")
        new_generation = 0
        self.sort()

        avr = 0.0
        for i in range( self.POPULATION_SIZE ):
            avr += self.population[i][1]
        avr /= self.POPULATION_SIZE


        while new_generation < int(0.3*self.POPULATION_SIZE) :
            t = self.select_for_tournament()
            t1 = self.crossover( t )
            t2 = self.crossover( t )
            self.unchecked_population.append([t[0][0], t1, 0])
            self.unchecked_population.append([t[1][0], t2, 0])
            new_generation += 2
#            new_generation.append(self.crossover(t))
#        self.population =  self.population[0:(self.POPULATION_SIZE - int(0.3*self.POPULATION_SIZE))] + new_generation
        

        self.unchecked_population.append([ self.POPULATION_SIZE-1, NeuralNetwork( 227, 3, 128, 32), 0 ] )

        self.dumps.write("POPULATION" + str(self.generation) + "#AVRG :" + str(avr) )
        self.generation +=1
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
