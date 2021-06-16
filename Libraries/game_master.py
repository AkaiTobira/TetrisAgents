import pygame
import time
import enum

from Libraries.Structures.tetrisGame import Tetris
from Libraries.game import Game
from Libraries.presenter import Presenter
from Libraries.tester import Tester
from Libraries.consts    import *

class GameState(Enum):
    LearningApp = 1,
    PresentingApp = 2,
    TestingApp = 3,

class StateChanger:
    activeApp    = None
    apps = {}

    def get_state(self, state):
        if state == GameState.LearningApp:
            if not 1 in self.apps.keys():
                self.apps[1] = Game((250,860), "Tetris")
            self.activeApp = self.apps[1]
            return self.activeApp
        if state == GameState.TestingApp:
            if not 3 in self.apps.keys():
                self.apps[3] = Tester((250,860), "Tetris")
            self.activeApp = self.apps[3]
            return self.activeApp
        if state == GameState.PresentingApp:
            if not 2 in self.apps.keys():
                self.apps[2] = Presenter((int(1300 * NUMBER_OF_SCREENS/5.0) ,860), "Tetris")
            self.activeApp = self.apps[2]
            return self.activeApp

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
            last_state = self.activeState
            if event.key == AppKeys.ChangeScreen:
                self.activeState = GameState.LearningApp
            if event.key == AppKeys.ChangeScreen2:
                self.activeState = GameState.PresentingApp
            if event.key == AppKeys.ChangeScreen3:
                self.activeState = GameState.TestingApp
            if last_state != self.activeState:
                self.activeScreen  = self.stateSwitcher.get_state(self.activeState)
                self.activeScreen.reset_resolution()

    def update(self, delta):
        self.activeScreen.update(delta)

    def draw(self,):
        self.activeScreen.draw()

    def is_running(self):
        return self.running