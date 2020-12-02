import pygame
import time

from Libraries.consts                import *
from Libraries.Structures.tetrisGame import Tetris
from Libraries.Structures.displayers  import FPSDisplayer
from Libraries.Structures.tetrominoSpawner import MultiRandomSpawner
from Libraries.Structures.playerList import PresenterBotsController

class Presenter:
    screen      = None
    resolution  = None
    name        = ""
    tetrisGames = None
    fpsRate     = None
    multispawner= None
    autorestart = False
    instantRestart = False
    playModes = None



    def __init_pygame(self, resolution, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def reset_resolution(self):
        self.__init_pygame(self.resolution,self.name)

    def __init__(self, resolution, name):
        self.resolution  = resolution
        self.name        = name
        self.reset_resolution()
        self.multispawner = MultiRandomSpawner(NUMBER_OF_SCREENS)
        self.playModes    = PresenterBotsController()

        self.fpsRate = FPSDisplayer (self.screen, [ OFFSET/2 + 6 + 100, OFFSET/2 +6 + (GRID_HEIGHT + 15) * SQUARE_SIZE ])
        self.tetrisGames = []
        for i in range( NUMBER_OF_SCREENS ):
            self.tetrisGames.append( Tetris(self.screen, [OFFSET/2 + 6 + 250 * i, OFFSET/2 +6], self.multispawner.get_spawner(i), self.playModes.getBotUnit(i) ))

    def is_running(self):
        return self.running

    def process(self, event):
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].process(event)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.resetAll()

            if event.key == pygame.K_w:
                self.autorestart = not self.autorestart 

            if event.key == pygame.K_e:
                self.instantRestart = not self.instantRestart 

    def draw(self):
        self.screen.fill(get_color(Colors.BLACK))
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].draw()
        self.fpsRate.draw_text(19)
        pygame.display.flip()

    def resetAll(self):
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].reset()

    def resetAll_Instant(self):
        for i in range(len(self.tetrisGames)):
            if self.tetrisGames[i].is_game_over : self.tetrisGames[i].reset()

    def restart(self):
        
        if self.instantRestart:
            self.resetAll_Instant()
            return

        RestartCounter = True
        for i in range( len(self.tetrisGames) ):
            RestartCounter &= self.tetrisGames[i].is_game_over

        if( RestartCounter ):
                self.resetAll()

    def update(self,  delta): 
        for i in range(len(self.tetrisGames)):
            self.tetrisGames[i].update(delta)
        if( self.autorestart ): self.restart()
        self.fpsRate.update(delta)    