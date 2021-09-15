import pygame
import math

from Libraries.Algoritms.alg_pso    import PSO
from Libraries.consts import *
from Libraries.Structures.settings import *

class PSOAi:
    pso_alg  = None
    current_values = [0,0,0,0]
    
    hights = [0,0,0,0,0,0,0,0,0,0]
    holes  = [0,0,0,0,0,0,0,0,0,0]

    def __init__(self, predefined_values = None):
        if( predefined_values == None):
            self.pso_alg        = PSO()
            self.current_values = self.pso_alg.particles[0].pos_v
        else:
            print( "PSOAgent", len(predefined_values), " Loaded best for presenter app :" + str(predefined_values) )
            self.current_values = predefined_values

    def try_fit(self, x_pos, t, grid):
        t.position[0] = x_pos

        while True:
            t.position[1] += 1
            if not t.is_valid(grid):
                t.position[1] -= 1
                grid.lock(t, get_color(Colors.GOLD))
                return self.evaulate(grid, t)

    def evaulate(self, grid, t):
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
        for i in range(len(self.current_values)):
            score += heuristicList[i] * self.current_values[i]

        return score

    def next_move(self, t, grid, _unused):
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
        if self.pso_alg == None: return
        #self.pso_alg.add_score(score, cleaned)
        self.current_values = self.pso_alg.get_next_to_check(score, cleaned)