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

class StateChanger:
    activeApp    = None
    inactiveApp  = None

    def get_state(self, state):
        if state == GameState.LearningApp:
            if self.activeApp == None: self.activeApp = Game((250,860), "Tetris")
            return self.activeApp
        if state == GameState.PresentingApp:
            if self.inactiveApp == None: self.inactiveApp  = Presenter((int(1300 * NUMBER_OF_SCREENS/5.0) ,860), "Tetris")
            return self.inactiveApp

class GameMaster:
    stateSwitcher = None
    activeScreen  = None
    activeState   = GameState.LearningApp
    running       = True

    def __init__(self):
        pygame.mouse.set_visible(False)
        self.stateSwitcher = StateChanger()
        self.activeScreen  = self.stateSwitcher.get_state(self.activeState)
        
    def process(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.NOEVENT: return
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.process_change_app(event)
            self.activeScreen.process(event)

    def process_change_app(self, event):
        if event.type == pygame.KEYUP:
            if event.key == AppKeys.ChangeScreen:
                self.change_app()

    def update(self, delta):
        self.activeScreen.update(delta)

    def draw(self,):
        self.activeScreen.draw()

    def is_running(self):
        return self.running

    def change_app(self):
        if self.activeState == GameState.LearningApp:
            self.activeState = GameState.PresentingApp

        elif self.activeState == GameState.PresentingApp:
            self.activeState = GameState.LearningApp

        self.activeScreen  = self.stateSwitcher.get_state(self.activeState)
        self.activeScreen.reset_resolution()
