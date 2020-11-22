import pygame

from Libraries.Structures.tetiomers  import *
from Libraries.Structures.grid_cell  import GridCell
from Libraries.consts     import *
from Libraries.Structures.displayers import ScoreDisplayer, NextTetiomerBox, HeuresticDisplayer
from random     import shuffle
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_nnetwork   import NeuralEvolutionAi
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Agents.agent_rlearning  import ReinforcmentLearning
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork

class TetrisGrid:
    grid = []

    heights    = [0,0,0,0,0,0,0,0,0,0]
    holes      = [0,0,0,0,0,0,0,0,0,0]

    clearedRow = 0
    maxColumn  = 0
    sumHeight  = 0
    sumHoles   = 0
    bumpiness  = 0

    def __init__(self):
        self.grid = []
        for i in range(GRID_WIDTH):
            self.grid.append([])
            for j in range(GRID_HEIGHT):
                self.grid[i].append(  get_color(Colors.BLACK) )

    def clone(self):
        t = TetrisGrid()
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                t[i][j] = get_color(Colors.BLACK) if self.grid[i][j] == get_color(Colors.BLACK) else get_color(Colors.GOLD)
        t.clearedRow = self.clearedRow
        t.maxColumn  = self.maxColumn
        t.sumHeight  = self.sumHeight
        t.sumHoles   = self.sumHoles
        t.bumpiness  = self.bumpiness
        return t        

    def __evaluate(self, tetromino):
        self.clearedRow = self.clear_full_rows(tetromino.position, tetromino.get_size())

        for i in range( 0, GRID_WIDTH):
            self.heights[i] = 0
            for j in range( 0, GRID_HEIGHT ):
                if self.grid[i][j] != get_color(Colors.BLACK): 
                    self.heights[i]  = abs( GRID_HEIGHT - j )
                    break

        for i in range(GRID_WIDTH):
            self.holes[i] = 0
            for j in range( 0, GRID_HEIGHT-1, 1):
                if self.grid[i][j] != get_color(Colors.BLACK) and self.grid[i][j+1] == get_color(Colors.BLACK):
                    self.holes[i] += 1
        
        self.maxColumn = max(self.heights)
        self.sumHeight = sum(self.heights)
        self.sumHoles  = sum(self.holes)
        self.bumpiness = 0

        for i in range( 0, GRID_WIDTH ):
            if not i == 0: self.bumpiness += math.fabs( self.heights[i-1] - self.heights[i] )

    def lock(self, tetromino, color=(255,215,0)):
        shape_size = tetromino.get_size()
        shape      = tetromino.get_shape()
        pos        = tetromino.position

        if tetromino.is_locked : return

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i]: self.grid[pos[0] + i][ pos[1] + j] = color
        self.__evaluate(tetromino)

    def _check_row(self, j):
        for i in range(GRID_WIDTH):
            if self.grid[ i ][ j ] == get_color(Colors.BLACK) : return False
        return True

    def find_rows_to_delete(self, pos, shape_size):
        rows_to_delete = []
        for j in range(shape_size[1], shape_size[3], 1):
            if self._check_row(pos[1] + j): rows_to_delete.append( pos[1] + j ) 
        return rows_to_delete

    def clear_full_rows(self, position, shape):
        rows_to_delete = self.find_rows_to_delete(position, shape)
        for i in range(len(rows_to_delete)):
            for j in range(GRID_WIDTH):
                del self.grid[j][rows_to_delete[i]]
                self.grid[j].insert(0,  get_color(Colors.BLACK) )
        return len(rows_to_delete)

    def remove_rows(self, rows_to_delete):
        for i in range(len(rows_to_delete)):
            for j in range(GRID_WIDTH):
                del self.grid[j][rows_to_delete[i]]
                self.grid[j].insert(0,  get_color(Colors.BLACK) )

    def unlock( self, tetromino): pass

    def __str__(self):
        s = ""
        for j in range( GRID_HEIGHT):
            for i in range(GRID_WIDTH): 
                s += "1 " if self.grid[i][j] == get_color(Colors.BLACK) else "0 "
            s += "\n"
        return s

    def __getitem__(self, i):
        return self.grid[i]

    def __setitem__(self, i, c):
        self.grid[i] = c



#from agent_experimental import PredifinedLearning

import math
import time

ROW_MULTIPLER = 1000000

class RandomSpawnTetromino:
    c_tetromino = None
    n_tetromino = None

    tetrominos = [ O(), N(),  Z(), T(), J(), L(),I()]
    index       = 0

    def __init__(self):
        shuffle(self.tetrominos)
        self.c_tetromino = self.tetrominos[0]
        self.n_tetromino = self.tetrominos[1]
        self.index       = 1

    def increment_index(self):
        self.index = (self.index+1) % 7

    def get_next(self):
        self.c_tetromino = self.n_tetromino
        self.increment_index()
        self.n_tetromino = self.tetrominos[self.index]
        
        if self.index == 0:
            #self.tetrominos = [O(),O(),O(),O(),O(),O(),O()]
            self.tetrominos = [ O(), N(),  Z(), T(), J(), L(), I()]
            shuffle(self.tetrominos)

class TetrisLogic:
    logic_grid      = None
    score           = 0
    def __init__(self):
        self.reset()

    def reset(self):
        self.score      = 0
        self.logic_grid = TetrisGrid()

    def get_grid(self): return self.logic_grid   

    def progress_tetromino(self, tetromino):
        tetromino.position[1] += 1
        if not tetromino.is_valid(self.logic_grid):
            tetromino.position[1] -= 1
            self.logic_grid.lock(tetromino, tetromino.color)
            self.score += 1
            if self.logic_grid.clearedRow != 0 :
                self.score += (2 ** ( self.logic_grid.clearedRow -1 )) * ROW_MULTIPLER
            return False
        return True

    def move_left(self, tetromino):
        if tetromino.position[0] > tetromino.get_position_range()[0]  :
            tetromino.position[0] -= 1
            if not tetromino.is_valid(self.logic_grid) : tetromino.position[0] += 1

    def rotate_right(self, tetromino):
        if tetromino.can_rotate:
            tetromino.rotate_right()

    def move_right(self, tetromino):
        if tetromino.position[0] < tetromino.get_position_range()[1]  :
            tetromino.position[0] += 1
            if not tetromino.is_valid(self.logic_grid) : tetromino.position[0] -= 1
        
    def rotate_left(self, tetromino):
        if tetromino.can_rotate:
            tetromino.rotate_left()

    def drop( self, tetromino):
        while self.progress_tetromino(tetromino): pass
        tetromino.is_locked = True

    def game_over(self):
        for i in range(GRID_WIDTH):
            if self.logic_grid[ i ][ 1 ] != get_color(Colors.BLACK) : return True
        return False

class TetrisDisplayers:
    screen = None
    color  = get_color(Colors.LIGHT_PURPLE)
    points = None
    future = None
    heures = None
    grid   = None

    def __init__(self, screen):
        self.screen = screen
        self.points = ScoreDisplayer    (screen, [ (GRID_WIDTH + 1) * SQUARE_SIZE + GRID_HEIGHT , SQUARE_SIZE + GRID_HEIGHT  ])
        self.future = NextTetiomerBox   (screen, [ (GRID_WIDTH + 1) * SQUARE_SIZE + GRID_HEIGHT , GRID_WIDTH/2 * SQUARE_SIZE ])
        self.heures = HeuresticDisplayer(screen, [ (GRID_WIDTH + 1) * SQUARE_SIZE + GRID_HEIGHT , (GRID_WIDTH/2  + 6) * SQUARE_SIZE ])

        self.grid       = []
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append( GridCell( screen , ( (i * SQUARE_SIZE) + OFFSET, (j * SQUARE_SIZE) + OFFSET )))

    def drawGrid(self):
        for i in range(GRID_WIDTH*GRID_HEIGHT):
            self.grid[i].draw()
        pygame.draw.rect(self.screen, self.color, [ OFFSET/2 + 6, OFFSET/2 +6 , (GRID_WIDTH * SQUARE_SIZE), (GRID_HEIGHT * SQUARE_SIZE) ], 2)	

    def draw(self):
        self.future.draw()
        self.points.draw()
        self.heures.draw()

    def _convert_index(self, i, j):
        return i * GRID_HEIGHT + j

    def synchronize_grid(self, grid):
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid[self._convert_index(i,j)].fill_cell(grid[i][j])   

    def synchronize_numbers(self, score, heuresitcs, values):
        self.heures.process(heuresitcs , values)
        self.points.process(score)

    def synchronize_tetromino(self, c_t , n_t):
        self._draw_tetromino_in_grid(c_t)
        self.future.process(n_t)
        
    def _draw_tetromino_in_grid(self, c_t):
        shape_size = c_t.get_size()
        shape      = c_t.get_shape()
        pos        = c_t.position

        if c_t.is_locked : return

        for i in range(shape_size[0], shape_size[2], 1):
            for j in range(shape_size[1], shape_size[3], 1):
                if shape[j][i]: self.grid[self._convert_index(pos[0] + i, pos[1] + j)].fill_cell( c_t.color)

class Tetris:

    score  = 0
    screen = None

    time_to_drop = 0.0
    drop_time    = 0.5

    spawner    = None
    logic      = None
    displayers = None

    enable_draw = True

    player_index  = 0
    players       = [ None,       EvolutionAi(), GradAi(),   PSOAi(),    ReinforcmentNetwork()] #NeuralEvolutionAi(), ReinforcmentLearning()]#, PredifinedLearning() ]
    players_keys  = [ pygame.K_1, pygame.K_2,    pygame.K_3, pygame.K_4, pygame.K_5           ] #pygame.K_5,          pygame.K_6,           ]#  pygame.K_7]

    number_of_tetrominos = 0

    def __init__(self, screen):
        self.spawner    = RandomSpawnTetromino()
        self.logic      = TetrisLogic()
        self.displayers = TetrisDisplayers(screen)
        self.reset()


    def reset(self):
        self.number_of_tetrominos = 0
        self.score  = 0
        self.spawner.get_next()
        self.logic.reset() 

    def draw(self):
        self.displayers.drawGrid()
        if self.enable_draw : 
            self.displayers.draw()

    def update(self, delta):
        self.displayers.synchronize_grid( self.logic.get_grid() )
        if self.enable_draw :
            self.displayers.synchronize_tetromino( self.spawner.c_tetromino, self.spawner.n_tetromino )

        self.time_to_drop += delta
        if self.time_to_drop > self.drop_time:
            if self.player_index == 0 : self.update_human_player()
            else : self.train_Ai()
            self.time_to_drop = 0.0

    def train_Ai(self):
        if not self.logic.progress_tetromino(self.spawner.c_tetromino):
            self.spawner.get_next()
            self.number_of_tetrominos += 1
            self.logic.score += self.players[self.player_index].select_bestMove(self.spawner.c_tetromino, self.logic.get_grid())* ROW_MULTIPLER
            self.score = self.logic.score
            if self.enable_draw : self.displayers.synchronize_numbers(self.score, [0,0,0,0,0,0,0], [1,1,1,1] )
        if self.logic.game_over() or self.number_of_tetrominos > 5000 :
            self.players[self.player_index].set_score(self.score, self.number_of_tetrominos)    
            self.reset()

    def update_human_player(self):
        if not self.logic.progress_tetromino(self.spawner.c_tetromino):
            self.spawner.get_next()
            self.score = self.logic.score
            if self.enable_draw : self.displayers.synchronize_numbers(self.score, [0,0,0,0,0,0,0], [1,1,1,1] )
        if self.logic.game_over(): self.reset()

    def process( self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.enable_draw = not self.enable_draw
                return

            for key_i in range(len(self.players_keys)):
                if event.key == self.players_keys[key_i]:
                    self.reset()
                    self.drop_time    = 1.0
                    self.player_index = key_i
                    if self.players[self.player_index]:
                        self.drop_time    = 0.0
                        self.players[self.player_index].select_bestMove(self.spawner.c_tetromino, self.logic.get_grid())
                        return
                        
            if event.key == pygame.K_z:
                self.drop_time = 0.0
            if event.key == pygame.K_p:
                self.drop_time = 100000
            if event.key == pygame.K_x:
                self.drop_time = 1.0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.logic.rotate_left(self.spawner.c_tetromino)
                return
            
            if event.key == pygame.K_UP:
                self.logic.rotate_right(self.spawner.c_tetromino)
                return

            if event.key == pygame.K_RIGHT:
                self.logic.move_right(self.spawner.c_tetromino)    
                return
            
            if event.key == pygame.K_LEFT:
                self.logic.move_left(self.spawner.c_tetromino)
                return

            if event.key == pygame.K_SPACE:
                self.logic.drop(self.spawner.c_tetromino)
                #self.spawner.get_next()
                return

