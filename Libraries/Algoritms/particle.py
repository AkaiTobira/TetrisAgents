
from random import uniform, randint
from math   import sqrt
from copy   import deepcopy
from Libraries.consts import DATE_TIME
from Libraries.vector import Vector

class Particle:
    dir_v      = None
    pos_v      = None
    best_pos   = None
    curr_score = 0
    best_score = -99999999 

    def __init__(self, nmberOfDimension=4, rangee=(-10000,10000), curr_score = 0):
        self.dir_v      = Vector(nmberOfDimension,unit=True)
        self.pos_v      = Vector(nmberOfDimension,unit=True)
        self.best_pos   = deepcopy(self.pos_v)
        self.curr_score = curr_score
        self.best_score = -99999999 

    def update_best(self):
        if(self.best_score < self.curr_score):
            self.best_pos = self.pos_v
            self.best_score = self.curr_score

    def move(self, team_best_pos, w, c1, c2):
        change = w * self.dir_v 
    #    print( w )
        change += c1*uniform(0.0,1.0)*( self.best_pos - self.pos_v ) 
        change += c2*uniform(0.0,1.0)*( team_best_pos - self.pos_v )
        self.dir_v = change.norm()
        self.pos_v = self.pos_v + change

    def __str__(self):
        return   "BS:" + str( self.best_score ) + "  CS:" + str( self.curr_score )

    def __repr__(self):
        return self.__str__()
