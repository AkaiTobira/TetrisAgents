import pygame
import time

from Libraries.consts                import *
from Libraries.Structures.tetrisGame import Tetris

class Presenter:
    screen      = None
    resolution  = None
    
    def __init_pygame(self, resolution, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def __init__(self, resolution, name):
        self.__init_pygame(resolution,name)
        self.resolution  = resolution
        self.tetris      = Tetris(self.screen)

    def is_running(self):
        return self.running

    def process(self, event):
        self.tetris.process(event)

    def draw(self):
        self.screen.fill(get_color(Colors.BLACK))
        self.tetris.draw()
        pygame.display.flip()

    def update(self,  delta): 
        self.tetris.update(delta)