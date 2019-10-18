import pygame
import time

from tetris      import Tetris
from consts      import *

class Game:
    screen      = None
    resolution  = None
    running     = True
    
    def __init_pygame(self, resolution, name):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def __init__(self, resolution, name):
        self.__init_pygame(resolution,name)
        self.running     = True
        self.resolution  = resolution
        self.tetris      = Tetris(self.screen)

    def is_running(self):
        return self.running

    def process(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT: return
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.tetris.process(event)

    def draw(self):
        self.screen.fill(get_color(Colors.BLACK))
        self.tetris.draw()
        pygame.display.flip()

    def update(self,  delta): 
        self.tetris.update(delta)