from Libraries.vector import Vector
from Libraries.Structures.settings import PARAMS
import pygame
import math

from Libraries.Algoritms.alg_evolution import EvolutionAlgoritm
from Libraries.Algoritms.alg_evolution2 import EvolutionAlgoritm2, VECTOR_INDEX
from Libraries.consts        import *
from Libraries.Structures.settings import *
import json
class EvolutionAi:
    evolution_alg  = None
    numberOfDimensions = 4
    isLocked = False
    current_values = [0,0,0,0]
    
    hights = [0,0,0,0,0,0,0,0,0,0]
    holes  = [0,0,0,0,0,0,0,0,0,0]

    binary_something = {}


    def __init__(self, predefined_values = None):
        if( predefined_values == None):
            self.evolution_alg  = EvolutionAlgoritm2()
            self.current_values = self.evolution_alg.get_first_to_check()
            if self.current_values is Vector:
                self.numberOfDimensions = len(self.current_values.v)
            else:
                self.numberOfDimensions = len(self.current_values)
        else:
            self.isLocked = True
            self.current_values = predefined_values
            self.numberOfDimensions = len(self.current_values)

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD), evaluate_immidetly = False )

                self.binary_something[(x_pos, t.current_rotate)] = [grid.to_int_list(), grid.clear_full_rows(t.position, t.get_size())]
                grid.wortk(t)
                grid.clearedRow = self.binary_something[(x_pos, t.current_rotate)][1]
                grid.fullSquares += (4 - grid.clearedRow*GRID_WIDTH)
                
                
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
        heuristicList = []
        if CLEARED_ROW_INDEX      in PARAMS.HEURYSTIC: heuristicList.append(grid.clearedRow)
        if MIN_COLUMN_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.minColumn)
        if MAX_COLUMN_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.maxColumn)
        if DIFF_COLUMN_INDEX      in PARAMS.HEURYSTIC: heuristicList.append(grid.diffColumn)
        if SUM_HEIGHT_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHeight)
        if AVG_HEIGHT_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.avgHeight)
        if SUM_HOLES_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHoles2)
        if SUM_HOLES2_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumHoles)
        if BUMPINESS_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.bumpiness)
        if BUMPINESS_HEIGHT_INDEX in PARAMS.HEURYSTIC: heuristicList.append(grid.bumpinessHeight)
        if H_TRANSITIONS_INDEX    in PARAMS.HEURYSTIC: heuristicList.append(grid.hTransitions)
        if V_TRANSITIONS_INDEX    in PARAMS.HEURYSTIC: heuristicList.append(grid.vTransitions)
        if BIG_WHEEL_INDEX        in PARAMS.HEURYSTIC: heuristicList.append(grid.biggestWheel)
        if SUM_WHEELS_INDEX       in PARAMS.HEURYSTIC: heuristicList.append(grid.sumWheel)
        if FULL_SQUARES_INDEX     in PARAMS.HEURYSTIC: heuristicList.append(grid.fullSquares)
        if TETRIMINO_POSITION     in PARAMS.HEURYSTIC: heuristicList.append(t.position[1])

        score = 0.0
        for i in range(self.numberOfDimensions):
            score += heuristicList[i] * self.current_values[i]
        return score

    def next_move(self, t, grid, _event):
        _grid = grid.get_grid()

        previous = _grid.to_int_list()

        best = [ -9999999.0, t.get_position_range()[0], 0]
        for j in range(0, t.max_rotate):
            for i in range( t.get_position_range()[0], t.get_position_range()[1] + 1):
                t.position = [3,0]
                v = self.try_fit( i, t, _grid.clone() )
                if v > best[0] : best = [v, i, t.current_rotate]
            if t.can_rotate : t.rotate_left()

        t.current_rotate =   best[2]
        t.position       = [ best[1], 0 ]

        memory_unit = [previous, self.binary_something[(best[1], t.current_rotate)][0], self.binary_something[(best[1], t.current_rotate)][1], False ]

        with open('Backups/idotiis' + '.json', 'a') as outfile:
            json.dump(memory_unit, outfile, indent=4)

        return 0

    def game_over_feedback(self, score, cleaned): 
        if self.isLocked : return
        self.evolution_alg.add_score(score * ROW_MULTIPLER, cleaned)
        self.current_values = self.evolution_alg.get_next_active()

