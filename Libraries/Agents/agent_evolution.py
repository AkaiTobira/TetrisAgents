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

    def __init__(self, predefined_values = None, numberOfDimenstions = 4, spawnerType = -1, numberOfGames = 8):
        self.numberOfDimensions = numberOfDimenstions
        if( predefined_values == None):
            self.evolution_alg  = EvolutionAlgoritm(numberOfDimenstions, spawnerType, numberOfGames)
            self.current_values = self.evolution_alg.unchecked_population[0][1]
        else:
            self.isLocked = True
            self.current_values = predefined_values
            self.numberOfDimensions = len(predefined_values)

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(t, grid)

    def evaluate_4(self, t, grid):
        return ( t.position[1] * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] #+ grid.clearedRow
                    )
    
    def evaluate_5(self, t, grid):
        return ( t.position[1] * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.clearedRow * self.current_values[4]
                    )

    def evaluate_6(self, t, grid):
        return ( grid.vTransitions * self.current_values[0] + 
                    grid.avgHeight * self.current_values[1] + 
                    grid.sumHoles2  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.bumpinessHeight * self.current_values[4] +
                    (GRID_HEIGHT - t.position[1])  * self.current_values[5]
                    )

    def evaluate_7(self, t, grid):
        return ( grid.vTransitions * self.current_values[0] + 
                    grid.avgHeight * self.current_values[1] + 
                    grid.sumHoles2  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.bumpinessHeight * self.current_values[4] +
                    (GRID_HEIGHT - t.position[1])  * self.current_values[5] +
                    grid.clearedRow * self.current_values[6]
                    )

    def evaluate_8(self, t, grid):
        return ( grid.vTransitions * self.current_values[0] + 
                    grid.hTransitions * self.current_values[1] + 
                    grid.biggestWheel  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.diffColumn * self.current_values[4] +
                    t.position[1]  * self.current_values[5] +
                    grid.avgHeight * self.current_values[6] +
                    grid.bumpinessHeight * self.current_values[7]
                    )
    def evaluate_10(self, t, grid):
        return ( grid.hTransitions * self.current_values[0] +
                grid.vTransitions * self.current_values[1] +
                t.position[1] * self.current_values[2] +
                grid.maxColumn   * self.current_values[3] + 
                grid.minColumn   * self.current_values[4] + 
                grid.avgHeight    * self.current_values[5] +
                grid.bumpiness    * self.current_values[6] +
                grid.clearedRow   * self.current_values[7] +
                grid.sumWheel     * self.current_values[8] +
                grid.bumpinessHeight  * self.current_values[9]
                )
    def evaluate_14(self, t, grid):
        return (
                    grid.hTransitions * self.current_values[0] +
                    grid.vTransitions * self.current_values[1] +
                    t.position[1] * self.current_values[2] +
                    grid.maxColumn   * self.current_values[3] + 
                    grid.minColumn   * self.current_values[4] + 
                    grid.avgHeight    * self.current_values[5] +
                    grid.sumHeight    * self.current_values[6] + 
                    grid.sumHoles2    * self.current_values[7] +
                    grid.bumpiness    * self.current_values[8] +
                    grid.clearedRow   * self.current_values[9] +
                    grid.sumWheel     * self.current_values[10] +
                    grid.biggestWheel * self.current_values[11] +
                    grid.bumpinessHeight  * self.current_values[12] +
                    grid.fullSquares  * self.current_values[13]
                    )


    def evaulate(self, t, grid):
        if  self.numberOfDimensions == 4: return self.evaluate_4(t,grid)
        if  self.numberOfDimensions == 5: return self.evaluate_5(t,grid)
        if  self.numberOfDimensions == 6: return self.evaluate_6(t,grid)
        if  self.numberOfDimensions == 8: return self.evaluate_8(t,grid)
        #if  self.numberOfDimensions == 7: return self.evaluate_7(t,grid)
        if self.numberOfDimensions == 14: return self.evaluate_14(t,grid)
        if self.numberOfDimensions == 10: return self.evaluate_10(t,grid)
        
        if  self.numberOfDimensions == 7:
            return ( grid.vTransitions * self.current_values[0] + 
                    grid.hTransitions * self.current_values[1] + 
                    grid.sumHoles2  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] +
                    grid.diffColumn * self.current_values[4] +
                    t.position[1]  * self.current_values[5] +
                    grid.avgHeight * self.current_values[6]
                    )
        
        
        print("No Valid type")
        return ( t.position[1] * self.current_values[0] + 
                    grid.sumHeight * self.current_values[1] + 
                    grid.sumHoles  * self.current_values[2] + 
                    grid.bumpiness * self.current_values[3] #+ grid.clearedRow
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
