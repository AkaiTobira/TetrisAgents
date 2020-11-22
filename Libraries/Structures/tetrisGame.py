

import pygame
from Libraries.Structures.tetrominoSpawner import RandomSpawnTetromino
from Libraries.Structures.tetris           import TetrisGrid, TetrisLogic, TetrisDisplayers
from Libraries.Structures.playerList       import PlymodeController
from Libraries.Structures.timerController  import TimerController
from Libraries.consts                      import *

class Tetris:

    score  = 0
    screen = None

    time_to_drop = 0.0
    drop_time    = 0.5

    spawner          = None
    logic            = None
    displayers       = None
    players_controll = None
    flow_controll    = None

    enable_draw = True

    number_of_tetrominos = 0

    def __init__(self, screen):
        self.spawner          = RandomSpawnTetromino()
        self.logic            = TetrisLogic()
        self.players_controll = PlymodeController()
        self.displayers       = TetrisDisplayers(screen, [OFFSET/2 + 6, OFFSET/2 +6])
        self.flow_controll    = TimerController(self.players_controll)
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
        self.displayers.synchronize_grid(self.logic.get_grid())
        self.displayers.synchronize_tetromino( self.spawner.c_tetromino, self.spawner.n_tetromino )
        self.displayers.synchronize_numbers( self.score )

        self.drop_time = self.flow_controll.getTimeDelay()

        self.time_to_drop += delta
        if self.time_to_drop > self.drop_time:
            self.update_board()
            self.time_to_drop -= self.drop_time

    def update_board(self):
        if not self.logic.progress_tetromino(self.spawner.c_tetromino):
            self.spawner.get_next()
            self.score = self.logic.score
            self.number_of_tetrominos += 1
        if self.logic.game_over() or self.number_of_tetrominos > MAX_NUMBER_PER_GAME: 
            self.players_controll.game_over_feedback(self.score, self.number_of_tetrominos)
            self.reset()

    def process(self, event):
        self.flow_controll.process(event)
        self.players_controll.process(event)
        self.displayers.process(event)

        self.logic.score += self.players_controll.get_active_player().next_move(self.spawner.c_tetromino, self.logic, event) * ROW_MULTIPLER


