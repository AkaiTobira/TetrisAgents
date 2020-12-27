import pygame
import math

from Libraries.Algoritms.alg_evolution import EvolutionAlgoritm
from Libraries.consts        import *

class EvolutionAi:
    evolution_alg  = None
    numberOfDimensions = 4
    isLocked = False
    current_values = [0,0,0,0]
    
    hights = [0,0,0,0,0,0,0,0,0,0]
    holes  = [0,0,0,0,0,0,0,0,0,0]

    def __init__(self, predefined_values = None, numberOfDimenstions = 4):
        self.numberOfDimensions = numberOfDimenstions
        if( predefined_values == None):
            self.evolution_alg  = EvolutionAlgoritm(numberOfDimenstions)
            self.current_values = self.evolution_alg.unchecked_population[0][1]
        else:
            self.isLocked = True
            print( "EvolutionAgent", numberOfDimenstions, " Loaded best for presenter app :" + str(predefined_values) )
            self.current_values = predefined_values

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(grid)

    def evaulate(self, grid):
        if self.numberOfDimensions == 4:
            return ( grid.biggestWheel * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] #+ grid.clearedRow
                    )
        if  self.numberOfDimensions == 5:
            return ( grid.maxColumn * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.biggestWheel * self.current_values[4]
                    )
        if  self.numberOfDimensions == 6:
            return ( grid.maxColumn * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.clearedRow * self.current_values[4] +
                    grid.biggestWheel * self.current_values[5]
                    )

    def next_move(self, t, grid, _event):
        _grid = grid.get_grid()

        best = [ -9999999.0, t.get_position_range()[0], 0]
        for j in range(0, t.max_rotate):
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1):
                t.position = [3,0]
                v = self.try_fit( i, t, _grid.clone() )
                if v > best[0] : best = [v, i, t.current_rotate]
            if t.can_rotate : t.rotate_left()

        t.current_rotate =   best[2]
        t.position       = [ best[1], 0 ]

        return 0

    def game_over_feedback(self, score, cleaned): 
        if self.isLocked : return
        self.evolution_alg.add_score(score * ROW_MULTIPLER, cleaned)
        self.current_values = self.evolution_alg.get_next_active()
