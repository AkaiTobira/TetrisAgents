from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from Libraries.consts import DATE_TIME

from Libraries.vector import Vector

class Particle:
    dir_v      = None
    pos_v      = None
    best_pos   = None
    best_score = -99999999 

    def __init__(self, nmberOfDimension=4, rangee=(-10000,10000)):
        self.dir_v      = Vector(nmberOfDimension,unit=True)
        self.pos_v      = Vector(nmberOfDimension,unit=True)
        self.best_pos   = deepcopy(self.pos_v)
        self.best_score = -99999999 

    def update_best(self, score):
        self.best_pos   = self.pos_v
        self.best_score = score

    def move(self, team_best_pos, w, c1, c2):
        change = w * self.dir_v 
        change += c1*uniform(0.0,1.0)*( self.best_pos - self.pos_v ) 
        change += c2*uniform(0.0,1.0)*( team_best_pos - self.pos_v )
        self.dir_v = change.norm()
        self.pos_v = self.pos_v + change

    def __str__(self):
        return  "#CPos: " +  str( self.pos_v) + "\n#BestPos: " + str(self.best_pos)+ "\n#CurrDir:" + str( self.dir_v ) + "\n#BestScore :" + str( self.best_score ) + "\n"

    def __repr__(self):
        return self.__str__()

class PSO:
    particles = []
    best_score = -999999
    best_pos   = None

    population_size = 0
    index           = 0
    iteraiton       = 0
    max_iteration   = 0.0

    to_check  = []

    ineria     = 0.9

    dumps = None
    moves = None

    def __init__(self, population_size, numberOfIteration=100):
        self.dumps = open("logs/pso/PSO_GEN_" + DATE_TIME, "w")
        self.moves = open("logs/pso/PSO_MOV_" + DATE_TIME, "w")

        self.best_pos = Vector(4)
        self.population_size = population_size
        self.max_iteration   = numberOfIteration
        for _ in range( population_size ): self.particles.append( Particle(4) )
        for particle in self.particles:    self.to_check.append( particle)

        self.dumps.write( "#GENERATION#" + str( self.iteraiton ) )
        for i in range( len(self.particles) ):
            self.dumps.write( str(i) + str( self.particles[i] ) )

    def get_next_to_check(self, score, cleaned):
        self.index += 1
        if self.index == self.population_size: 
            self.index = 0
            self.iteraiton += 1.0
            if self.ineria < 0.001 : self.ineria = 0
            else : self.ineria = ( 0.4 ) - ( 0.4 ) * ( self.iteraiton / self.max_iteration ) 

            self.dumps.write( "#GENERATION#" + str( self.iteraiton ) )
            for i in range( len(self.particles) ):
                self.dumps.write( str(i) + str( self.particles[i] ) )

        self.moves.write( str(self.index) + "#" + str(score) + "#" + str((cleaned/30.0))[:5] + "%#" + str(self.to_check[0].pos_v) + "#\n" )

        if score > self.to_check[0].best_score: 
            self.moves.write( str(self.index) + "#IMPROVES_SCORE#" + str(self.to_check[0].best_pos) + "#\n" )
            self.to_check[0].update_best(score)
        if score > self.best_score: 
            self.moves.write( str(self.index) + "#IMPROVES_TEAM_SCORE#FROM:" + str(self.best_pos) + "#TO" +  str(self.to_check[0].best_pos) + "#OLDSCORE#" + str(self.best_score) + "\n"  )
            self.best_score = score
            self.best_pos   = self.to_check[0].best_pos
        
        self.to_check[0].move(self.best_pos, self.ineria, 1.5,1)
        self.to_check.append(self.to_check[0])
        del self.to_check[0]

        return self.to_check[0].pos_v
