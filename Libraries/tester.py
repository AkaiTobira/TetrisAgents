
from random import Random, random, SystemRandom
from Libraries.Algoritms.alg_nn import NeuralNetwork
import pygame
import time

from Libraries.consts                import *
from Libraries.Structures.tetrisGame import Tetris
from Libraries.Structures.displayers  import FPSDisplayer
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Structures.playerList import PresenterBotUnit
from Libraries.Structures.tetrominoSpawner import NewestRandomSpawnTetromino, RandomSpawnTetromino, SimpleSpawnTetrimino
from Libraries.Structures.tetrominoSpawner import MultiRandomSpawner
from Libraries.Structures.playerList       import PlymodeController, PlymodeControllerTester
from Libraries.Structures.playerList import PresenterBotsController
from Libraries.Structures.meansures  import Meansures
from Libraries.Structures.best_saver import BestUnitsBackupSaver

MAX_NUMBER_OF_GAMES = 100

class PlayedGamesChecker:
    index = 1
    meansureName = 0
    

    def __init__(self) -> None: pass
        #with open('logs/scores/bestBackup.json', 'w') as outfile:
        #    json.dump(self.json_converted, outfile, indent=4)

    def get_first_not_completed(self):
        keys = BestUnitsBackupSaver.json_converted.keys()
        Meansures.register_meansure("Timer_GameLenght")

        for key in keys:
            for generator in range(2,3):
                try :
                    with open('logs/scores/' + str(key) + "-" + str(generator), 'r') as infile:
                        num_lines = sum(1 for line in infile)
                        if num_lines > MAX_NUMBER_OF_GAMES: continue
                        self.index = num_lines
                        infile.close()
                        return key, generator
                except IOError:
                    self.create_template(key, generator)
                    return key, generator

        return list(keys)[int(random() * len(keys))], int(random() * 3)

    def create_template(self, key, generator):
        with open('logs/scores/' + str(key) + "-" + str(generator), 'w') as outfile:
            outfile.write(str(key) + "-" + str(generator) + ",score,tetriminos,game time\n")
        outfile.close()
        self.index = 1

    def log_score(self, key, generator, score, tetriminos):
        with open('logs/scores/' + str(key) + "-" + str(generator), 'r') as infile:
            self.index = sum(1 for line in infile)
        infile.close()

        with open('logs/scores/' + str(key) + "-" + str(generator), 'a') as outfile:
            outfile.write(str(self.index) + "," + str(score)+"," + str(tetriminos) + "," + str(Meansures.lap_meansure("Timer_GameLenght")) + "\n")
        outfile.close()
        print( str(key) + "-" + str(generator) + ":" + str(self.index) + "," + str(score)+"," + str(tetriminos))
        return self.index > MAX_NUMBER_OF_GAMES


class ContinuesPlaymodeController:
    playerUnit = None
    spawner    = None
    checker    = PlayedGamesChecker()

    first_not_over = ""
    generatorType  = ""

    def __init__(self):
        self.spawner =  RandomSpawnTetromino()
        self.create_next_unit()
        #print(self.playerUnit, self.spawner)

    def _get_spawner(self):
        if self.generatorType == 0: return SimpleSpawnTetrimino()
        if self.generatorType == 1: return RandomSpawnTetromino()
        if self.generatorType == 2: return NewestRandomSpawnTetromino()

    def create_next_unit(self): 
        self.first_not_over, self.generatorType = self.checker.get_first_not_completed()
        print(self.first_not_over, self.generatorType)
        self.playerUnit = self.create_player()
        self.spawner = self._get_spawner()

    def create_player(self):
        alg = None
        if "Evo" in self.first_not_over: alg = EvolutionAi(BestUnitsBackupSaver.getLastBest(self.first_not_over))
        if "PSO" in self.first_not_over: alg = PSOAi(BestUnitsBackupSaver.getLastBest(self.first_not_over))
        if "Neu" in self.first_not_over: alg = ReinforcmentNetwork(BestUnitsBackupSaver.getLastBest(self.first_not_over))
        return alg

    def get_max_limit(self): return 9999999999

    def get_player(self, playerIndex): return self.playerUnit

    def get_active_player(self): return self.playerUnit

    def get_spawner(self): return self.spawner

    def game_over_feedback(self, score, number_of_tetrominos): 
        ine = self.checker.log_score(self.first_not_over, self.generatorType, score, number_of_tetrominos)
        if ine : self.create_next_unit()

    def player_changed(self): return False

    def process(self, event): pass
    
    def is_AI_Player(self): return True

class Tester:
    screen      = None
    resolution  = None
    name        = ""
    fpsRate     = None

    playmodeController = None

    def __init_pygame(self, resolution, name):
        pygame.display.set_caption(name)
        self.screen = pygame.display.set_mode(resolution)
    
    def reset_resolution(self):
        self.__init_pygame(self.resolution,self.name)

    def __init__(self, resolution, name):
        self.name = name
        self.resolution  = resolution
        self.reset_resolution()
        self.playmodeController = ContinuesPlaymodeController()
        self.tetris  = Tetris(self.screen, [OFFSET/2 + 6, OFFSET/2 +6], SimpleSpawnTetrimino(), self.playmodeController)
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