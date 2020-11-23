import pygame
import math

from Libraries.Algoritms.alg_evolution import EvolutionAlgoritm
from Libraries.consts        import *

class EvolutionAi:
    evolution_alg  = None
    current_values = [0,0,0,0]
    
    hights = [0,0,0,0,0,0,0,0,0,0]
    holes  = [0,0,0,0,0,0,0,0,0,0]

    def __init__(self):
        self.evolution_alg  = EvolutionAlgoritm()
        self.current_values = self.evolution_alg.unchecked_population[0][1]

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        mins = max( x_pos, 0)
        maxs = min( x_pos + 4, GRID_WIDTH)
        importantHeights = grid.heights[mins: maxs]
        pos_y = max( math.fabs(GRID_HEIGHT - max( importantHeights )) - 4, 0 )
        t.position[1] = int(pos_y)

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(grid)

    def evaulate(self, grid):
        return ( grid.maxColumn * self.current_values[0] + 
                 grid.sumHeight * self.current_values[1] + 
                 grid.sumHoles  * self.current_values[2] + 
                 grid.bumpiness * self.current_values[3] #+ grid.clearedRow
                 )

    def next_move(self, t, grid, _event):
        grid = grid.get_grid()
        best = [ -9999999.0, t.get_position_range()[0], 0]
        for j in range(0, t.max_rotate):
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1):
                t.position = [3,0]
                v = self.try_fit( i, t, grid.clone() )
                if v > best[0] : best = [v, i, t.current_rotate]
            if t.can_rotate : t.rotate_left()

        t.current_rotate =   best[2]
        t.position       = [ best[1], 0 ]
        return 0

    def game_over_feedback(self, score, cleaned): 
        self.evolution_alg.add_score(score, cleaned)
        self.current_values = self.evolution_alg.get_next_active()
