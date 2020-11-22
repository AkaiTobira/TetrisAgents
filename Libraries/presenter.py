import pygame
import time

from Libraries.consts                import *
from Libraries.Structures.tetrisGame import Tetris
from Libraries.Structures.displayers  import FPSDisplayer

class Presenter:
    screen      = None
    resolution  = None
    name        = ""
    tetrisGames = None
    fpsRate     = None

    def __init_pygame(self, resolution, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def reset_resolution(self):
        self.__init_pygame(self.resolution,self.name)

    def __init__(self, resolution, name):
        self.resolution  = resolution
        self.name        = name
        self.reset_resolution()

        self.fpsRate = FPSDisplayer (self.screen, [ OFFSET/2 + 6 + 100, OFFSET/2 +6 + (GRID_HEIGHT + 15) * SQUARE_SIZE ])
        self.tetrisGames = []
        for i in range( 5 ):
            self.tetrisGames.append( Tetris(self.screen, [OFFSET/2 + 6 + 250 * i, OFFSET/2 +6]))

    def is_running(self):
        return self.running

    def process(self, event):
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].process(event)

    def draw(self):
        self.screen.fill(get_color(Colors.BLACK))
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].draw()
        self.fpsRate.draw_text(19)
        pygame.display.flip()

    def update(self,  delta): 
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].update(delta)
        self.fpsRate.update(delta)    