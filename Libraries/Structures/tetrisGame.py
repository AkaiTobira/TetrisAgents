

import pygame
from Libraries.Structures.tetrominoSpawner import RandomSpawnTetromino
from Libraries.Structures.tetris           import TetrisGrid, TetrisLogic, TetrisDisplayers
from Libraries.Structures.playerList       import PlymodeController
from Libraries.Structures.timerController  import TimerController
from Libraries.consts                      import *


class Logger:
    files = [] 
    active = -1

    def __init__(self):
        self.files = [ 
            open("logs/ooo1.txt", "w"),
            open("logs/ooo2.txt", "w"),
            open("logs/ooo3.txt", "w"),
            open("logs/ooo0.txt", "w"),
        ]

    def getNext(self):
        self.active += 1
        return self.files[self.active]

lllll = Logger()

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

    enable_draw  = True
    is_game_over = False 

    number_of_tetrominos = 0



    def __init__(self, screen, position, spawner, playerlist):
        self.spawner          = spawner
        self.logic            = TetrisLogic()
        self.players_controll = playerlist
        self.displayers       = TetrisDisplayers(screen, position, self.logic.get_grid() )
        self.flow_controll    = TimerController(self.players_controll)
        self.reset()


    def reset(self):
        self.number_of_tetrominos = 0
        self.score  = 0
        self.spawner.reset()
        self.logic.reset() 
        self.displayers.setGrid( self.logic.get_grid() )
        self.is_game_over = False

    def draw(self):
        self.displayers.drawGrid()
        self.displayers.draw()

    def update(self, delta):
        if self.is_game_over : return

        self.displayers.synchronize_grid(self.logic.get_grid())
        self.displayers.synchronize_tetromino( self.spawner.c_tetromino, self.spawner.n_tetromino )
        self.displayers.synchronize_numbers( self.score, self.number_of_tetrominos )

        self.drop_time = self.flow_controll.getTimeDelay()

        self.time_to_drop += delta
        if self.time_to_drop > self.drop_time:
            self.update_board()
            self.time_to_drop -= self.drop_time

        if self.players_controll.is_AI_Player():
            addToScore = self.players_controll.get_active_player().next_move(self.spawner.c_tetromino, self.logic, None)
            
            self.logic.score += addToScore
            self.logic.drop(self.spawner.c_tetromino)


    def update_board(self):
        if not self.logic.progress_tetromino(self.spawner.c_tetromino):
            self.spawner.get_next()
            self.score = self.logic.score
            self.number_of_tetrominos += 1
        if self.logic.game_over() or self.number_of_tetrominos > MAX_NUMBER_PER_GAME: 
            self.players_controll.game_over_feedback(self.score, self.number_of_tetrominos)
            self.spawner.disable()
            self.is_game_over = True

    def process(self, event):
        self.flow_controll.process(event)
        self.players_controll.process(event)
        self.displayers.process(event)

        if not self.players_controll.is_AI_Player():
            self.logic.score += self.players_controll.get_active_player().next_move(self.spawner.c_tetromino, self.logic, event)


