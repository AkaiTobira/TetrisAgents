import pygame

from Libraries.Agents.agent_human      import HumanPlayer
from Libraries.Agents.agent_grad       import GradAi
from Libraries.Agents.agent_evolution  import EvolutionAi
from Libraries.Agents.agent_nnetwork   import NeuralEvolutionAi
from Libraries.Agents.agent_pso        import PSOAi
from Libraries.Agents.agent_rlearning  import ReinforcmentLearning
from Libraries.Agents.agent_rnetwork   import ReinforcmentNetwork
from Libraries.Structures.best_saver   import BestUnitsBackupSaver
from Libraries.consts import NUMBER_OF_SCREENS

class PlymodeController:
    learning_modes = {}
    last_pressed_player_key = pygame.K_1
    current_active_player_key = pygame.K_1
    switching_enabled = True

    def __init__( self, switch_enabled = True ):
        self.switching_enabled = switch_enabled
        self.learning_modes = {
            pygame.K_1 : HumanPlayer(),
            pygame.K_2 : EvolutionAi(None, 4),
            pygame.K_3 : EvolutionAi(None, 5),
            pygame.K_4 : EvolutionAi(None, 6),
            pygame.K_5 : PSOAi(None, 4),
            pygame.K_6 : PSOAi(None, 5),
            pygame.K_7 : PSOAi(None, 6)
        #    pygame.K_6 : ReinforcmentNetwork(),
        }
        self.actors_names ={
            pygame.K_1 : "Active Player : Human",
            pygame.K_2 : "Active Player : EvolutionAi4",
            pygame.K_3 : "Active Player : EvolutionAi5",
            pygame.K_4 : "Active Player : EvolutionAi6",
            pygame.K_5 : "Active Player : PSOAi4",
            pygame.K_6 : "Active Player : PSOAi5",
            pygame.K_7 : "Active Player : PSOAi6",
            pygame.K_8 : "Active Player : NeuralNetwork" 
        }

    def player_changed(self):
        player_changed = self.last_pressed_player_key != self.current_active_player_key
        if player_changed : print(self._get_active_player_name())
        self.current_active_player_key = self.last_pressed_player_key
        return player_changed

    def _get_active_player_name(self):
        return self.actors_names[self.last_pressed_player_key]


    def get_player(self, playerIndex):
        return self.learning_modes[self.learning_modes.keys[playerIndex]]

    def get_active_player(self):
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
            PresenterBotUnit(EvolutionAi( BestUnitsBackupSaver.getLastBest("Evolution4"), 4 )),
            PresenterBotUnit(EvolutionAi( BestUnitsBackupSaver.getLastBest("Evolution5"), 5 )),
            PresenterBotUnit(PSOAi( BestUnitsBackupSaver.getLastBest("PSO4") , 4)),
            PresenterBotUnit(PSOAi( BestUnitsBackupSaver.getLastBest("PSO5") , 5)),                    
            PresenterBotUnit(PSOAi( BestUnitsBackupSaver.getLastBest("PSO6") , 6)),
            
            PresenterBotUnit(EvolutionAi( BestUnitsBackupSaver.getLastBest("Evolution6"), 6 )),
            PresenterBotUnit(EvolutionAi( BestUnitsBackupSaver.getLastBest("Evolution6") )),
        ]
        self.bots = self.bots[ : NUMBER_OF_SCREENS ]

    def getBotUnit( self, index ): 
        return self.bots[index]


class PresenterBotUnit:
    playerUnit = None

    def __init__( self, bot ): 
        self.playerUnit = bot

    def get_player(self, playerIndex): return self.playerUnit

    def get_active_player(self): return self.playerUnit

    def game_over_feedback(self, score, number_of_tetrominos): pass

    def player_changed(self): return False

    def process(self, event): pass
    
    def is_AI_Player(self): return True


