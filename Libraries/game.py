import pygame
import time

from Libraries.consts                      import *
from Libraries.Structures.tetrisGame       import Tetris
from Libraries.Structures.displayers       import FPSDisplayer
from Libraries.Structures.tetrominoSpawner import RandomSpawnTetromino, SimpleSpawnTetrimino
from Libraries.Structures.playerList       import PlymodeController
from Libraries.Structures.meansures        import Meansures

class Game:
    screen      = None
    resolution  = None
    name        = ""
    fpsRate     = None

    def __init_pygame(self, resolution, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def reset_resolution(self):
        self.__init_pygame(self.resolution,self.name)

    def __init__(self, resolution, name):
        self.name = name
        self.resolution  = resolution
        self.reset_resolution()
        self.tetris  = Tetris(self.screen, [OFFSET/2 + 6, OFFSET/2 +6], SimpleSpawnTetrimino(), PlymodeController())
        self.fpsRate = FPSDisplayer (self.screen, [ OFFSET/2 + 6 + 100, OFFSET/2 +6 + (GRID_HEIGHT + 15) * SQUARE_SIZE ])

    def is_running(self):
        return self.running

    def process(self, event):
        self.tetris.process(event)

    def draw(self):
        self.screen.fill(get_color(Colors.BLACK))
        self.tetris.draw()
        self.fpsRate.draw_text(19)
        pygame.display.flip()

    def update(self,  delta): 
        if self.tetris.is_game_over: self.tetris.reset()
        self.tetris.update(delta)
        Meansures.tick()
        self.fpsRate.update(delta)