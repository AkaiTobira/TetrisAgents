import pygame
import time
import enum

from Libraries.Structures.tetrisGame import Tetris
from Libraries.game import Game
from Libraries.presenter import Presenter
from Libraries.consts    import *

class GameState(Enum):
    LearningApp = 1,
    PresentingApp = 2

class GameMaster:
    activeApp    = None
    inactiveApp  = None
    activeState  = GameState.LearningApp
    running      = True

    def __init__(self):
        pygame.mouse.set_visible(False)
        self.inactiveApp  = Presenter((1300,860), "Tetris")
        self.activeApp    = Game((250,860), "Tetris")

    def process(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT: return
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.process_change_app(event)
            self.activeApp.process(event)

    def process_change_app(self, event):
        if event.type == pygame.KEYUP:
            if event.key == AppKeys.ChangeScreen:
                self.change_app()

    def update(self, delta):
        self.activeApp.update(delta)

    def draw(self,):
        self.activeApp.draw()


    def is_running(self):
        return self.running

    def change_app(self):
        if self.activeState == GameState.LearningApp:
            self.activeState = GameState.PresentingApp

        elif self.activeState == GameState.PresentingApp:
            self.activeState = GameState.LearningApp
            
        temp = self.activeApp
        self.activeApp = self.inactiveApp
        self.inactiveApp = temp

        self.activeApp.reset_resolution()
