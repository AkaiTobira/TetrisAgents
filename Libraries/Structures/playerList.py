import pygame

from Libraries.Agents.agent_human      import HumanPlayer
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_nnetwork   import NeuralEvolutionAi
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Agents.agent_rlearning  import ReinforcmentLearning
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork
from Libraries.Structures.best_saver   import BestUnitsBackupSaver
from Libraries.Structures.tetrominoSpawner import MultipleSpawnTetromino, NewestRandomSpawnTetriminoLocked, SimpleSpawnTetrimino, RandomSpawnTetromino, NewestRandomSpawnTetromino, NewestRandomSpawnTetriminoLocked
from Libraries.consts import NUMBER_OF_SCREENS, MAX_NUMBER_PER_GAME_HUM, MAX_NUMBER_PER_GAME_EVO, MAX_NUMBER_PER_GAME_PSO, MAX_NUMBER_PER_GAME_NN

class PlymodeController:
    learning_modes = {}
    last_pressed_player_key = pygame.K_1
    current_active_player_key = pygame.K_1
    switching_enabled = True

    def __init__( self, switch_enabled = True ):
        self.switching_enabled = switch_enabled
        self.learning_modes = {
            pygame.K_1 : None,
            pygame.K_2 : None,
            pygame.K_3 : None,
            pygame.K_4 : None,
            pygame.K_5 : None,
            pygame.K_6 : None,
            pygame.K_7 : None,
            pygame.K_0 : None,
            pygame.K_9 : None,
            pygame.K_8 : None
        }
        self.actors_names ={
            pygame.K_1 : "Active Player : Human",
            pygame.K_2 : "Active Player : EvolutionAi10 - SimpleRandomizer",
            pygame.K_3 : "Active Player : EvolutionAi10 - EasyRandomizer",
            pygame.K_4 : "Active Player : EvolutionAi10 - NewestRandomizer",
            pygame.K_5 : "Active Player : PSOAi10 - SimpleRandomizer",
            pygame.K_6 : "Active Player : PSOAi10 - EasyRandomizer",
            pygame.K_7 : "Active Player : PSOAi10 - NewestRandomizer",
            pygame.K_8 : "Active Player : ReinforcmentNetwork - SimpleRandomizer",
            pygame.K_9 : "Active Player : ReinforcmentNetwork - EasyRandomizer",
            pygame.K_0 : "Active Player : ReinforcmentNetwork - NewestRandomizer"
        }

    def player_changed(self):
        player_changed = self.last_pressed_player_key != self.current_active_player_key
    #    if player_changed : print(self._get_active_player_name())
        self.current_active_player_key = self.last_pressed_player_key
        return player_changed

    def _get_active_player_name(self):
        return self.actors_names[self.last_pressed_player_key]

    def _init_player(self, keyId):
        if keyId == pygame.K_1 : return HumanPlayer()
        if keyId == pygame.K_2 : return PSOAi(None, 7, 20, 0.5, 1.0, 0.4)
        if keyId == pygame.K_3 : return PSOAi(None, 7, 20, 0.5, 0.5, 0.5)
        if keyId == pygame.K_4 : return PSOAi(None, 7, 20, 1.5, 1.5, 0.6)
        if keyId == pygame.K_5 : return PSOAi(None, 7, 20, 1.5, 1.5, 0.7)
        if keyId == pygame.K_6 : return PSOAi(None, 7, 20, 1.5, 1.5, 0.8)
        if keyId == pygame.K_7 : return PSOAi(None, 7, 20, 1.5, 1.5, 0.9)
        if keyId == pygame.K_8 : return EvolutionAi(None, 7, 3, 8)
        if keyId == pygame.K_9 : return PSOAi(None, 6, 3)
        if keyId == pygame.K_6 : return PSOAi(None, 6, 2)
        if keyId == pygame.K_7 : return PSOAi(None, 6, 3)
        if keyId == pygame.K_8 : return ReinforcmentNetwork(None, 1)
        if keyId == pygame.K_9 : return ReinforcmentNetwork(None, 2)
        if keyId == pygame.K_0 : return ReinforcmentNetwork(None, 3)

    def get_max_limit(self):
        if self.current_active_player_key == pygame.K_1 : return MAX_NUMBER_PER_GAME_HUM
        if self.current_active_player_key == pygame.K_2 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_3 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_4 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_5 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_6 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_7 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_8 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_9 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_0 : return MAX_NUMBER_PER_GAME_NN

    def get_spawner(self):
        if self.current_active_player_key == pygame.K_1 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_2 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_3 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_4 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_5 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_6 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_7 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_8 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_9 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_0 : return NewestRandomSpawnTetromino()

    def get_player(self, playerIndex):
        keyId = self.learning_modes.keys[playerIndex]
        if self.learning_modes[keyId] == None: 
            self.learning_modes[keyId] = self._init_player(keyId)
        return self.learning_modes[keyId]

    def get_active_player(self):
        if self.learning_modes[self.last_pressed_player_key] == None: 
            self.learning_modes[self.last_pressed_player_key] = self._init_player(self.last_pressed_player_key)
        return self.learning_modes[self.last_pressed_player_key]

    def game_over_feedback(self, score, number_of_tetrominos):
        self.learning_modes[self.last_pressed_player_key].game_over_feedback(score, number_of_tetrominos)

    def process(self, event):
        if not self.switching_enabled : return
        if event.type == pygame.KEYUP:
            if event.key in self.learning_modes.keys():
                toList = list(self.learning_modes.keys())
                index = toList.index(event.key)
                self.last_pressed_player_key = toList[index]

    def is_AI_Player(self):
        return self.last_pressed_player_key != pygame.K_1

class PlymodeControllerTester:
    learning_modes = {}
    last_pressed_player_key = pygame.K_1
    current_active_player_key = pygame.K_1
    switching_enabled = True

    def __init__( self, switch_enabled = True ):
        self.switching_enabled = switch_enabled
        self.learning_modes = {
            pygame.K_1 : None,
            pygame.K_2 : None,
            pygame.K_3 : None,
            pygame.K_4 : None,
            pygame.K_5 : None,
            pygame.K_6 : None,
            pygame.K_7 : None,
            pygame.K_0 : None,
            pygame.K_9 : None,
            pygame.K_8 : None
        }
        self.actors_names ={
            pygame.K_1 : "Active Player : Human",
            pygame.K_2 : "Active Player : EvolutionAi10 - SimpleRandomizer",
            pygame.K_3 : "Active Player : EvolutionAi10 - EasyRandomizer",
            pygame.K_4 : "Active Player : EvolutionAi10 - NewestRandomizer",
            pygame.K_5 : "Active Player : PSOAi10 - SimpleRandomizer",
            pygame.K_6 : "Active Player : PSOAi10 - EasyRandomizer",
            pygame.K_7 : "Active Player : PSOAi10 - NewestRandomizer",
            pygame.K_8 : "Active Player : ReinforcmentNetwork - SimpleRandomizer",
            pygame.K_9 : "Active Player : ReinforcmentNetwork - EasyRandomizer",
            pygame.K_0 : "Active Player : ReinforcmentNetwork - NewestRandomizer"
        }

    def player_changed(self):
        player_changed = self.last_pressed_player_key != self.current_active_player_key
    #    if player_changed : print(self._get_active_player_name())
        self.current_active_player_key = self.last_pressed_player_key
        return player_changed

    def _get_active_player_name(self):
        return self.actors_names[self.last_pressed_player_key]

    def _init_player(self, keyId):
        if keyId == pygame.K_1 : return HumanPlayer()
        if keyId == pygame.K_2 : return PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_1"), 6, 1), NewestRandomSpawnTetromino()),
        if keyId == pygame.K_3 : return PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_2"), 6, 2), SimpleSpawnTetrimino()),
        if keyId == pygame.K_4 : return PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_3"), 6, 3), RandomSpawnTetromino()),
        if keyId == pygame.K_5 : return PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_4"), 6, 4), NewestRandomSpawnTetromino()),
        if keyId == pygame.K_6 : return PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution14_3"), 14, 3), NewestRandomSpawnTetromino()),

        if keyId == pygame.K_3 : return EvolutionAi(None, 6, 2)
        if keyId == pygame.K_4 : return EvolutionAi(None, 6, 3)
        if keyId == pygame.K_5 : return EvolutionAi(None, 6, 4)
        if keyId == pygame.K_6 : return EvolutionAi(None, 14, 3)
        #if keyId == pygame.K_6 : return PSOAi(None, 6, 2)
        #if keyId == pygame.K_7 : return PSOAi(None, 6, 3)
       # if keyId == pygame.K_8 : return ReinforcmentNetwork(None, 1)
        #if keyId == pygame.K_9 : return ReinforcmentNetwork(None, 2)
       # if keyId == pygame.K_0 : return ReinforcmentNetwork(None, 3)

    def get_max_limit(self):
        if self.current_active_player_key == pygame.K_1 : return MAX_NUMBER_PER_GAME_HUM
        if self.current_active_player_key == pygame.K_2 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_3 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_4 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_5 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_6 : return MAX_NUMBER_PER_GAME_EVO
        if self.current_active_player_key == pygame.K_7 : return MAX_NUMBER_PER_GAME_PSO
        if self.current_active_player_key == pygame.K_8 : return MAX_NUMBER_PER_GAME_NN
        if self.current_active_player_key == pygame.K_9 : return MAX_NUMBER_PER_GAME_NN
        if self.current_active_player_key == pygame.K_0 : return MAX_NUMBER_PER_GAME_NN

    def get_spawner(self):
        if self.current_active_player_key == pygame.K_1 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_2 : return SimpleSpawnTetrimino()
        if self.current_active_player_key == pygame.K_3 : return RandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_4 : return NewestRandomSpawnTetriminoLocked()
        if self.current_active_player_key == pygame.K_5 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_6 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_7 : return NewestRandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_8 : return SimpleSpawnTetrimino()
        if self.current_active_player_key == pygame.K_9 : return RandomSpawnTetromino()
        if self.current_active_player_key == pygame.K_0 : return NewestRandomSpawnTetromino()

    def get_player(self, playerIndex):
        keyId = self.learning_modes.keys[playerIndex]
        if self.learning_modes[keyId] == None: 
            self.learning_modes[keyId] = self._init_player(keyId)
        return self.learning_modes[keyId]

    def get_active_player(self):
        if self.learning_modes[self.last_pressed_player_key] == None: 
            self.learning_modes[self.last_pressed_player_key] = self._init_player(self.last_pressed_player_key)
        return self.learning_modes[self.last_pressed_player_key]

    def game_over_feedback(self, score, number_of_tetrominos):
        self.learning_modes[self.last_pressed_player_key].game_over_feedback(score, number_of_tetrominos)

    def process(self, event):
        if not self.switching_enabled : return
        if event.type == pygame.KEYUP:
            if event.key in self.learning_modes.keys():
                toList = list(self.learning_modes.keys())
                index = toList.index(event.key)
                self.last_pressed_player_key = toList[index]

    def is_AI_Player(self):
        return self.last_pressed_player_key != pygame.K_1


class PresenterBotsController:
    bots = []

    def __init__( self ): 
        self.bots = [    
            PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_3"), 6, 3), NewestRandomSpawnTetriminoLocked()),
            PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_4"), 6, 4), NewestRandomSpawnTetriminoLocked()),
            PresenterBotUnit(EvolutionAi(BestUnitsBackupSaver.getLastBest("Evolution6_4"), 6, 4), NewestRandomSpawnTetriminoLocked()),
        ]
        self.bots = self.bots[ : NUMBER_OF_SCREENS ]

    def getBotUnit( self, index ): 
        return self.bots[index]

class PresenterBotUnit:
    playerUnit = None
    spawner    = None

    def __init__( self, bot, spawner ): 
        self.playerUnit = bot
        self.spawner = spawner

    def get_player(self, playerIndex): return self.playerUnit

    def get_active_player(self): return self.playerUnit

    def get_spawner(self): return self.spawner

    def game_over_feedback(self, score, number_of_tetrominos): pass

    def player_changed(self): return False

    def process(self, event): pass
    
    def is_AI_Player(self): return True


